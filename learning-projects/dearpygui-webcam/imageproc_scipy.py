import numpy as np
from scipy.ndimage import rotate

from app import ImageProcessor


class ScipyImageProcessor(ImageProcessor):

    def rotate(self, image: np.ndarray, degrees: float) -> np.ndarray:
        new_image = rotate(input=image, angle=degrees, reshape=False)
        assert image.shape == new_image.shape
        return new_image
    
    def adjust_brightness(self, image: np.ndarray, brightness: int) -> np.ndarray:
        return np.clip((image.astype(dtype=np.uint16) + brightness), a_min=0, a_max=255).astype(np.uint8)