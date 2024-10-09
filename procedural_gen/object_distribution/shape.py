import cv2
import numpy as np

from easy_kit.timing import time_func
from easy_raster.transform.morphology import binary_dilation


class Shape:

    @staticmethod
    def random(width: int, height: int):
        buffer = np.zeros((height, width))
        buffer[np.random.random_sample((height, width)) > .65] = 1
        return Shape(buffer)

    @staticmethod
    def circle(radius: int):
        ksize = 2 * radius + 1
        if ksize % 2 == 0:
            ksize += 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(ksize, ksize))
        return Shape(kernel)

    @time_func
    def __init__(self, buffer: np.ndarray):
        self.buffer = np.zeros_like(buffer)
        self.buffer[buffer > 0] = 1
        self.xx, self.yy = np.where(self.buffer > 0)

    @property
    def height(self):
        return self.buffer.shape[0]

    @property
    def width(self):
        return self.buffer.shape[1]

    @time_func
    def dilate(self, buffer: np.ndarray):
        buffer = binary_dilation(buffer, self.buffer).astype('uint8')
        return buffer

    def dilated(self):
        buffer = np.zeros((self.height * 2 + 1, self.width * 2 + 1))
        self.draw(self.width, self.height, buffer)
        return Shape(self.dilate(buffer))

    @time_func
    def draw(self, x: int, y: int, buffer: np.ndarray):
        coord_x = self.xx + x - self.width // 2
        coord_y = self.yy + y - self.height // 2
        ok = np.where((0 < coord_x) & (coord_x < buffer.shape[1]) & (0 < coord_y) & (coord_y < buffer.shape[0]))[0]
        buffer[coord_y[ok], coord_x[ok]] = 1
