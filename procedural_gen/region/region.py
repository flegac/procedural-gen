from dataclasses import dataclass, field
from typing import Self

import numpy as np

from easy_kit.timing import time_func
from procedural_gen.region.interval import Interval
from procedural_gen.region.vec import Vec


@dataclass
class Region:
    region: list[Interval] = field(default_factory=lambda: [Interval() for _ in range(3)])

    @staticmethod
    def convex(positions: list[Vec]):
        x1 = min([_.x for _ in positions])
        x2 = max([_.x for _ in positions])
        y1 = min([_.y for _ in positions])
        y2 = max([_.y for _ in positions])
        z1 = min([_.z for _ in positions])
        z2 = max([_.z for _ in positions])
        return Region(region=[
            Interval(start=x1, end=x2),
            Interval(start=y1, end=y2),
            Interval(start=z1, end=z2),
        ])

    @staticmethod
    def from_center(center: Vec = None, radius: float = .5):
        if center is None:
            center = Vec()
        return Region(region=[Interval.from_center(x, radius) for x in center])

    @staticmethod
    def from_size(width: float, height: float, depth: float = 1):
        return Region(region=[Interval.from_size(_) for _ in [width, height, depth]])

    @property
    def x(self):
        return self.region[0]

    @property
    def y(self):
        return self.region[1]

    @property
    def z(self):
        return self.region[2]

    @property
    def start(self):
        return Vec(vec=[_.start for _ in self])

    @property
    def end(self):
        return Vec(vec=[_.end for _ in self])

    @property
    def center(self):
        return Vec(vec=[_.center for _ in self])

    @property
    def radius(self):
        return Vec(vec=[_.radius for _ in self])

    @property
    def size(self):
        return Vec(vec=[_.size for _ in self])

    def interpolate(self, offset: Vec):
        return Vec(vec=[_.interpolate(x) for _, x in zip(self, offset)])

    def random(self):
        return Region(region=[_.random() for _ in self])

    def start_at(self, offset: Vec):
        return Region(region=[_.start_at(x) for _, x in zip(self, offset)])

    def end_at(self, offset: Vec):
        return Region(region=[_.end_at(x) for _, x in zip(self, offset)])

    def center_at(self, offset: Vec):
        return Region(region=[Interval.from_center(x, _.radius) for _, x in zip(self, offset)])

    def translate(self, offset: Vec):
        return Region(region=[_.translate(x) for _, x in zip(self, offset)])

    def select(self, origin: Self):
        return Region(region=[
            s.select(o) for s, o in zip(self, origin)
        ])

    @time_func
    def coords(self, width: int, height: int, depth: int = 1):
        return np.meshgrid(*[_.coords(size) for _, size in zip(self, [width, height, depth])])

    def split(self, width: int, height: int, depth: int = 1):
        splits = [_.split(size) for _, size in zip(self, [width, height, depth])]

        return [
            Region(region=list(region))
            for region in zip(*splits)
        ]

    def __repr__(self):
        return 'x'.join([f'{_}' for _ in self])

    def __str__(self):
        return repr(self)

    def __iter__(self):
        return iter(self.region)
