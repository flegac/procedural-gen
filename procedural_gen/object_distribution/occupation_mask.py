import random

import cv2
import numpy as np

from easy_kit.timing import time_func, timing
from easy_raster.model.position import Position
from easy_raster.model.resolution import Resolution
from easy_raster.transform.buffer_util import BufferUtil
from procedural_gen.object_distribution.object_instance import ObjectInstance
from procedural_gen.object_distribution.shape import Shape


class OccupationMask:
    def __init__(self, buffer: np.ndarray):
        self.resolution = Resolution.from_raw(*buffer.shape)
        self.mask = buffer
        self.reset_mask: np.ndarray = buffer.copy()

    @staticmethod
    def from_resolution(resolution: Resolution):
        return OccupationMask(buffer=resolution.new_buffer())

    @staticmethod
    def from_buffer(buffer: np.ndarray):
        return OccupationMask(buffer)

    def reset(self):
        self.mask = self.resolution.new_buffer()
        if self.reset_mask is not None:
            self.mask[self.reset_mask == 1] = 1

    def dilate(self, shape: Shape):
        return OccupationMask(shape.dilate(self.mask))

    @time_func
    def prepare_map(self, selection: np.ndarray, treshold: float, value: int = 1):
        with timing('ItemMap.prepare_map'):
            selection = BufferUtil.resize(selection, resolution=self.resolution)
            self.mask[selection < treshold] = value

    def circle(self, item: ObjectInstance, extra_radius: float = 0):
        cv2.circle(
            img=self.mask,
            center=self.resolution.rescale_position(item.position),
            radius=self.resolution.rescale_size(item.radius + extra_radius),
            color=[1 + item.object_id],
            thickness=-1
        )

    @time_func
    def search_position(self, max_rejects: int = 1000):
        for rejects in range(max_rejects):
            position = Position.random()
            if self.is_free(position):
                return position

        if len(np.nonzero(self.mask == 0)) / self.mask.size < 1 / max_rejects:
            free = self.compute_free(self.mask)
            if len(free) == 0:
                return
            val = random.choice(list(free))
            return Position.from_raw(val[1] / self.resolution.height, val[0] / self.resolution.width)

    def is_free(self, position: Position):
        x, y = self.resolution.rescale_position(position)
        return self.mask[y, x] == 0

    @time_func
    def compute_free(self, buffer: np.ndarray) -> set[tuple[int, int]]:
        return set(map(tuple, np.transpose(np.nonzero(buffer == 0))))
