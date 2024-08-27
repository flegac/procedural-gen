import math
from math import floor
from typing import Callable

import numpy as np

from easy_kit.timing import time_func, TimingTestCase
from procedural_gen.noise.fractal_sum import FractalSum
from procedural_gen.noise.interpolators import Interpolators, Interpolator
from procedural_gen.noise.point import Point
from procedural_gen.textures.textures import Textures


class ValueNoise:
    def __init__(
            self,
            grid_size: int,
            seed: int = 2210,
            interpolator: Interpolator = Interpolators.inter_cos
    ):
        self.size = grid_size
        self.interpolator = interpolator
        np.random.seed(seed)
        self.grid = np.random.rand(grid_size, grid_size)

    @time_func
    def noise2(self, point: Point) -> float:
        scaled = (point * self.size) % self.size

        x0 = floor(scaled.x)
        y0 = floor(scaled.y)

        x1 = (x0 + 1) % self.size
        y1 = (y0 + 1) % self.size

        v1 = self.grid[x0, y0]
        v2 = self.grid[x0, y1]
        v3 = self.grid[x1, y0]
        v4 = self.grid[x1, y1]

        return self.interpolator.interpolate2d(scaled, (v1, v2, v3, v4))


def save_noise(name: str, size: int, noise: Callable[[Point], ...], tiles: tuple[int, int] = (1, 1)):
    data = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            p = Point(x / size, y / size)
            data[x, y] = noise(p)
    data = np.tile(data, tiles)
    Textures.gray().dump_png(f'{name}_{size}', data)


class TestIt(TimingTestCase):
    def test_it(self):

        for interpolator in [
            Interpolators.round,
            # Interpolators.identity,
            Interpolators.poly_6x5_15x4_10x3,
            # Interpolators.inter_cos
        ]:
            base_noise = ValueNoise(grid_size=32, interpolator=interpolator)

            noise2 = base_noise.noise2

            # def noise2(p: Point):
            #     return Modifier.wood(base_noise.noise2(p))

            # save_noise(name=f'noise_{interpolator.__class__.__name__}', size=512, noise=base_noise.noise2)

            for power in [.5]:
                fbm = FractalSum(noise2).fbm(layers=6, lacunarity=math.pi * .5, power=power)
                save_noise(name=f'fbm_1', size=512, noise=fbm)
