import numpy as np
from scipy.ndimage import rotate

from app import ImageProcessor


class ScipyImageProcessor(ImageProcessor):

    def rotate(self, image: np.ndarray, degrees: float) -> np.ndarray:
        new_image = rotate(input=image, angle=degrees, reshape=False)
        assert image.shape == new_image.shape
        return new_image