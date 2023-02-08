""" Created on Wed Feb 08 16:13:49 2023

Core utils for Vibrio Detector

@author: Malik Anhar Maulana
"""
from typing import Tuple


def estimate_vibrio_size(
    image_shape: Tuple[int, int],
    vibrio_shape: Tuple[int, int],
) -> float:
    """
    Estimate the size of Vibrio by using relativity concept.

    Parameters
    ----------
    image_shape: Tuple[int, int]
        Image shape with format (height, width)
    vibrio_shape: Tuple[int, int]
        Vibrio shape with format (height, width)

    Return
    ------
    float
        Estimated size / diameter of Vibrio in milimeter
    """

    # The area of the cup is 7854 mm^2 so the radius of the cup is 49.98 mm,
    # and the diameter of the cup is 99.96 mm.
    cup_diameter = 99.96

    # Calculate the `milimeter per-pixel` by dividing the diameter of cup with
    # the minimum size of the `image_shape` assuming the image fits the cup.
    mm_pp = cup_diameter / min(image_shape)

    # To calculate the size of vibrio, we used the maximum size of its shape
    # and multiply it with the `milimeter per-pixel`
    return max(vibrio_shape) * mm_pp
