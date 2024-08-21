import random
from dataclasses import dataclass
from numbers import Number
from typing import Self, Any

import numpy as np

from easy_lib.timing import time_func


@dataclass
class Interval:
    start: float = 0
    end: float = 1

    @property
    def center(self):
        return (self.start + self.end) * .5

    @property
    def radius(self):
        return self.size * .5

    @property
    def size(self):
        return self.end - self.start

    @staticmethod
    def cast(item: Any):
        if isinstance(item, Number):
            return Interval(start=item, end=item)
        if isinstance(item, tuple):
            return Interval(start=item[0], end=item[1])
        if isinstance(item, Interval):
            return item
        raise ValueError(f'invalid type: {type(item)}')

    @staticmethod
    def from_center(center: float = 0, radius: float = .5):
        return Interval(start=center - radius, end=center + radius)

    @staticmethod
    def from_size(size: float = 1):
        return Interval(start=0, end=size)

    @time_func
    def interpolate(self, offset: float):
        return self.start + offset * self.size

    @time_func
    def random(self):
        start = self.start + random.random() * self.size
        end = start + random.random() * (self.end - start)
        return Interval(
            start=start,
            end=end
        )

    def start_at(self, offset: float):
        return Interval(start=offset, end=offset + self.size)

    def end_at(self, offset: float):
        return Interval(start=offset - self.size, end=offset)

    def center_at(self, offset: float):
        return Interval.from_center(offset, self.radius)

    def translate(self, offset: float):
        return Interval(start=self.start + offset, end=self.end + offset)

    def select(self, origin: Self):
        return Interval(
            start=origin.interpolate(self.start),
            end=origin.interpolate(self.end)
        )

    @time_func
    def coords(self, n: int):
        return np.array(np.linspace(self.start, self.end, n, dtype='float'))

    def split(self, n: int):
        coords = self.coords(n + 1)
        return [
            Interval(start=coords[i], end=coords[i + 1])
            for i in range(n)
        ]

    def __repr__(self):
        return f'[{self.start:.3f},{self.end:.3f}]'

    def __str__(self):
        return repr(self)

    def __add__(self, other: Self | Number):
        other = self.cast(other)
        return Interval(start=self.start + other.start, end=self.end + other.end)

    def __sub__(self, other: Self | Number):
        other = self.cast(other)
        return Interval(start=self.start - other.start, end=self.end - other.end)

    def __mul__(self, other: Self | Number):
        other = self.cast(other)
        return Interval(start=self.start * other.start, end=self.end * other.end)

    def __truediv__(self, other: Self | Number):
        other = self.cast(other)
        return Interval(start=self.start / other.start, end=self.end / other.end)
