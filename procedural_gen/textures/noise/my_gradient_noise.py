import math
import random
from typing import Callable


def poly_6x5_15x4_10x3(t: float):
    return 1 - t * t * t * (t * (t * 6 - 15) + 10)


class Gradient:
    def __init__(self, seed: int = 0, period: int = 2048):
        self.period = period
        random.seed(seed)
        self.perm = list(range(period))
        random.shuffle(self.perm)
        self.perm += self.perm
        self.dirs = [
            (math.cos(a * 2 * math.pi / period),
             math.sin(a * 2 * math.pi / period))
            for a in range(period)
        ]

    def hash(self, gx: int, gy: int, period: int):
        return self.perm[self.perm[gx % period] + gy % period]

    def gradient(self, gx: int, gy: int, x: float, y: float, period: int):
        hashed = self.hash(gx, gy, period)
        grad = (x - gx) * self.dirs[hashed][0] + (y - gy) * self.dirs[hashed][1]
        return grad


class SimplexNoise:
    def __init__(
            self,
            gradient: Gradient = None,
            interpolator: Callable[[float], float] = poly_6x5_15x4_10x3
    ):
        self.gradient = gradient or Gradient()
        self.interpolator = interpolator

    def noise(self, x: float, y: float, period: int):
        gx = int(x)
        gy = int(y)

        def surflet(ox: int, oy: int):
            grad = self.gradient.gradient(gx + ox, gy + oy, x, y, period)

            dx = abs(gx + ox - x)
            dy = abs(gy + oy - y)
            return self.interpolator(dx) * self.interpolator(dy) * grad

        return (
                surflet(0, 0)
                + surflet(1, 0)
                + surflet(0, 1)
                + surflet(1, 1)
        )

    def fbm(self, x: float, y: float, octaves: int, period: int):
        val = 0
        for o in range(octaves):
            lacunarity_o = 2 ** o
            val += .5 ** o * self.noise(x * lacunarity_o, y * lacunarity_o, period * lacunarity_o)
        return val
