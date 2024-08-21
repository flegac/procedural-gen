import math
from abc import ABC, abstractmethod

import numpy as np

from procedural_gen.noise.point import Point


class Interpolator(ABC):

    @abstractmethod
    def apply(self, t: float):
        ...

    def interpolate2d(self, scaled: Point, values: tuple[float, float, float, float]):
        x = self.apply(scaled.x % 1)
        y = self.apply(scaled.y % 1)

        i1 = np.interp(y, (0, 1), values[:2])
        i2 = np.interp(y, (0, 1), values[2:])
        res = np.interp(x, (0, 1), (i1, i2))

        return res

    def interpolate_grid2d(self, scaled: Point, values: tuple[float, float, float, float]):
        x = self.apply(scaled.x % 1)
        y = self.apply(scaled.y % 1)

        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)

        i1 = np.interp(y, (0, 1), values[:2])
        i2 = np.interp(y, (0, 1), values[2:])
        res = np.interp(x, (0, 1), (i1, i2))

        return res


class Identity(Interpolator):

    def apply(self, t: float):
        return t


class Round(Interpolator):

    def apply(self, t: float):
        return int(t)


class Poly_6x5_15x4_10x3(Interpolator):

    def apply(self, t: float):
        return t * t * t * (t * (t * 6 - 15) + 10)


class CosInterpolator(Interpolator):

    def apply(self, t: float):
        return .5 * (1 - np.cos(t * math.pi))


class Interpolators:
    identity = Identity()
    round = Round()
    poly_6x5_15x4_10x3 = Poly_6x5_15x4_10x3()
    inter_cos = CosInterpolator()
