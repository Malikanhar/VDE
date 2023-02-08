""" Created on Wed Feb 08 11:29:18 2023

Vibrio Detector based on HSV image filtering

@author: Malik Anhar Maulana
"""
import logging
from typing import Dict

import cv2
import numpy as np

from detector.image_process import mask_image, remove_noise, resize_keep_ratio
from detector.utils.util import add_log_handler
from detector.utils.core import estimate_vibrio_size


class VibrioDetector():
    """
    Vibrio Detector class.
    This detector laverage the HSV color space to localize the vibrio.

    Parameters
    ----------
    max_image_size: int
        maximum image size, if the image size is larger than `max_image_size`
        it will be resized to the `max_image_size` to reduce the computation.

    Return
    ------
    """

    def __init__(
            self,
            max_image_size: int = 480,
    ) -> None:

        self._logger = logging.Logger('VibrioDetector')
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False
        add_log_handler(self._logger, logging.INFO)
        self._logger.info(
            'Initializing Vibrio Detector...')

        if max_image_size <= 0:
            raise ValueError("'max_image_size' couldn't be <= 0!")

        self._max_image_size = max_image_size
        self._lower_yellow = np.array([15, 120, 110])
        self._upper_yellow = np.array([36, 255, 255])

    def preprocess_image(
            self,
            image: np.ndarray,
    ) -> np.ndarray:
        """
        Preprocess the image.

        Parameters
        ----------
        image: np.ndarray
            Input image to be processed

        Return
        ------
        np.ndarray
            Processed image
        """

        # Resize the image to the `max_image_size` to reduce computation
        resized_img = resize_keep_ratio(
            image=image, max_size=self._max_image_size)

        # Make the image smoother
        # resized_img = cv2.blur(resized_img, (5, 5))

        # Mask the image to localize the vibrio
        masked_img = mask_image(
            image=resized_img,
            lower_hsv_pixels=self._lower_yellow,
            upper_hsv_pixels=self._upper_yellow)

        # Remove noice from the masked image
        masked_img = remove_noise(image=masked_img)
        return masked_img

    def detect_vibrio_by_contour(
            self,
            image: np.ndarray,
            normalize_output: bool = True,
    ) -> Dict[str, list]:
        """
        Get detection of vibrio by using contour of the masked image.

        Parameters
        ----------
        image: np.ndarray
            Masked image
        normalize_output: bool
            Normalize the bounding box of detection results

        Return
        ------
        Dict[str, list]
            Detection results of `boxes` and `box_attributes`
        """
        img_h, img_w = image.shape[:2]
        detection = []
        detection_attributes = []
        contours, _ = cv2.findContours(
            image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = w / h

            # Filter the `aspect_ratio` to remove outlier
            if 0.5 <= aspect_ratio <= 1.5:
                x2 = x + w
                y2 = y + h
                detection.append([x, y, x2, y2])
                detection_attributes.append({
                    'class': 'vibrio-yellow',
                    'size': estimate_vibrio_size(
                        image_shape=(img_h, img_w),
                        vibrio_shape=(h, w),
                    ),
                })

        detection = np.asarray(detection, dtype=np.float32)

        # Normalize the detection output
        if normalize_output:
            detection[:, 0::2] = detection[:, 0::2] / img_w
            detection[:, 1::2] = detection[:, 1::2] / img_h

        return {
            'boxes': detection,
            'box_attributes': detection_attributes,
        }

    def run(
            self,
            image: np.ndarray,
    ) -> Dict[str, list]:

        # Preprocess the input image
        processed_image = self.preprocess_image(image)

        # Count vibrio by using the contour of masked image
        detection = self.detect_vibrio_by_contour(processed_image)

        return detection
