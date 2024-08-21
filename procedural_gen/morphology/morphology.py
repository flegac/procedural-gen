from abc import ABC, abstractmethod

import cv2
import numpy as np

from image_io.buffer_util import BufferUtil
from image_io.image_io import ImageIO


class Morph(ABC):

    @classmethod
    def square(cls, size: int, iterations: int = 1):
        kernel = np.ones((size, size), np.uint8)
        return cls(kernel=kernel, iterations=iterations)

    @classmethod
    def disc(cls, size: int, iterations: int = 1):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
        kernel = np.array(kernel)
        kk = BufferUtil.normalize(kernel)
        return cls(kernel=kernel, iterations=iterations)

    def __init__(self, kernel: np.ndarray, iterations: int = 1):
        self.kernel = kernel
        self.iterations = iterations

    def __call__(self, buffer: np.ndarray):
        return self.apply(buffer)

    @abstractmethod
    def apply(self, buffer: np.ndarray):
        ...


class Dilate(Morph):
    def apply(self, buffer: np.ndarray):
        return cv2.dilate(buffer, self.kernel, iterations=self.iterations)


class Erode(Morph):
    def apply(self, buffer: np.ndarray):
        return cv2.erode(buffer, self.kernel, iterations=self.iterations)


class Opening(Morph):
    def apply(self, buffer: np.ndarray):
        erode = Erode(self.kernel, self.iterations)
        dilate = Dilate(self.kernel, self.iterations)
        return dilate(erode(buffer))


class Closing(Morph):
    def apply(self, buffer: np.ndarray):
        erode = Erode(self.kernel, self.iterations)
        dilate = Dilate(self.kernel, self.iterations)
        return erode(dilate(buffer))
