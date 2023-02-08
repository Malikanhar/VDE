""" Created on Wed Feb 08 11:36:11 2023

Image processing helper for Vibrio Detector

@author: Malik Anhar Maulana
"""
from typing import Dict, Tuple, Optional

import cv2
import numpy as np


def resize_keep_ratio(
    image: np.ndarray,
    max_size: int = 480,
) -> np.ndarray:
    """
    Resize the image to the `max_size` of its width / height.

    Parameters
    ----------
    image: np.ndarray
        Input image
    max_size: int
        Target size of the resized image

    Return
    ------
    np.ndarray
        Resized image
    """
    h, w = image.shape[:2]

    if h > w:
        r = h / max_size
        new_w = int(w / r)
        new_h = max_size
    else:
        r = w / max_size
        new_h = int(h / r)
        new_w = max_size
    return cv2.resize(image, (new_w, new_h))


def mask_image(
    image: np.ndarray,
    lower_hsv_pixels: np.ndarray,
    upper_hsv_pixels: np.ndarray,
) -> np.ndarray:
    """
    Mask the input image using the HSV color space and filter out the pixel
    that out of range of `lower_hsv_pixels` and `upper_hsv_pixels`.

    Parameters
    ----------
    image: np.ndarray
        Input image with shape of (H, W, C) in RGB order
    lower_hsv_pixels: np.ndarray
        Lower bound of hsv pixels with shape of (3, )
    upper_hsv_pixels: np.ndarray
        Upper bound of hsv pixels with shape of (3, )

    Return
    ------
    np.ndarray
        Masked image with shape of (H, W)
    """

    # convert BGR image to HSV for color descriptor
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # create mask range using lower and upper hsv pixels
    mask = cv2.inRange(
        hsv_image, lower_hsv_pixels, upper_hsv_pixels)

    # Mask the input image for the yellow vibrio
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    masked_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)

    return masked_image


def remove_noise(
    image: np.ndarray,
) -> None:
    """
    Remove noise from the image by using erosion and dilation process.

    Parameters
    ---------
    image: np.ndarray
        Input image

    Return
    ------
    np.ndarray
        Processed image
    """
    proc_image = erode_image(image)
    proc_image = dilate_image(proc_image)
    return proc_image


def erode_image(
    image: np.ndarray,
) -> np.ndarray:
    """
    Image erosion process to remove noise from the masked image

    Parameters
    ----------
    image: np.ndarray
        Input masked image with shape of (H, W)

    Return
    ------
    np.ndarray
        Eroded image
    """
    kernel = np.ones((3, 3), np.uint8)
    img_erosion = cv2.erode(image, kernel, iterations=1)
    return img_erosion


def dilate_image(
    image: np.ndarray,
) -> np.ndarray:
    """
    Image dilation process to restore the vibrio size after erosion process

    Parameters
    ----------
    image: np.ndarray
        Input masked image with shape of (H, W)

    Return
    ------
    np.ndarray
        Dilated image
    """
    kernel = np.ones((3, 3), np.uint8)
    img_dilation = cv2.dilate(image, kernel, iterations=1)
    return img_dilation


def draw_bboxes(
    image: np.ndarray,
    detection: Dict[str, list],
    is_normalized: bool = True,
) -> np.ndarray:
    """
    Draw bounding box on the image.

    Parameters
    ----------
    image: np.ndarray
        Input image
    detection: Dict[str, list]
        Detection results of `boxes` and `box_attributes`
    is_normalized: bool
        Set it to True if the detection value has a range of [0, 1]

    Return
    ------
    np.ndarray
        Processed image with bounding box
    """
    boxes = np.asarray(detection['boxes'].copy())
    # Denormalize the bounding boxes
    if is_normalized:
        img_h, img_w = image.shape[:2]
        boxes[:, 0::2] = boxes[:, 0::2] * img_w
        boxes[:, 1::2] = boxes[:, 1::2] * img_h
        boxes = boxes.astype(int)

    image_osd = image.copy()
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(image_osd, (x1, y1), (x2, y2), (255, 0, 0), 1)
    return image_osd


def draw_contours(
        image: np.ndarray,
        contours: Tuple[Optional[np.ndarray]],
) -> np.ndarray:
    """
    Draw contours on the image.

    Parameters
    ----------
    image: np.ndarray
        Input image
    contours: Tuple[Optional[np.ndarray]]
        Tuple of contour

    Return
    ------
    np.ndarray
        Processed image with contour
    """
    img_osd = image.copy()
    return cv2.drawContours(img_osd, contours,  -1, (255, 0, 0), 1)


def draw_labels(
    image: np.ndarray,
    detection: Dict[str, list],
    is_normalized: bool = True,
) -> np.ndarray:
    """
    Draw bounding box on the image.

    Parameters
    ----------
    image: np.ndarray
        Input image
    detection: Dict[str, list]
        Detection results of `boxes` and `box_attributes`
    is_normalized: bool
        Set it to True if the detection value has a range of [0, 1]

    Return
    ------
    np.ndarray
        Processed image with bounding box
    """
    boxes = np.asarray(detection['boxes'].copy())
    box_attr = np.asarray(detection['box_attributes'])
    # Denormalize the bounding boxes
    if is_normalized:
        img_h, img_w = image.shape[:2]
        boxes[:, 0::2] = boxes[:, 0::2] * img_w
        boxes[:, 1::2] = boxes[:, 1::2] * img_h
        boxes = boxes.astype(int)

    image_osd = image.copy()
    for (x1, y1, x2, y2), box_attr in zip(boxes, box_attr):
        cv2.putText(
            image_osd,
            text='{:.2} mm'.format(box_attr['size']),
            org=(x1, y1-10),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=0.6,
            color=(0, 0, 0),
            thickness=1,
            lineType=cv2.LINE_AA)
    return image_osd
