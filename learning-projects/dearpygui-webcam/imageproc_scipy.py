import functools
import numpy as np
from scipy.ndimage import rotate

from app import ImageProcessor

def check_is_uint8(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> np.ndarray:
        image = func(*args, **kwargs)
        if image.dtype != np.uint8:
            raise TypeError(f"Expected uint8, got {image.dtype}")
        return image
    return wrapped


class ScipyImageProcessor(ImageProcessor):

    @check_is_uint8
    def rotate(self, image: np.ndarray, degrees: float) -> np.ndarray:
        new_image = rotate(input=image, angle=degrees, reshape=False)
        assert image.shape == new_image.shape
        return new_image
    
    @check_is_uint8
    def adjust_brightness(self, image: np.ndarray, brightness: int) -> np.ndarray:
        return np.clip((image.astype(dtype=np.uint16) + brightness), a_min=0, a_max=255).astype(np.uint8)