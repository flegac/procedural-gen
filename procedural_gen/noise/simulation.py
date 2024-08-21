# Semi-phisically-based hydraulic erosion simulation. Code is inspired by the
# code found here:
#   http://ranmantaru.com/blog/2011/10/08/water-erosion-on-heightmap-terrain/
# With some theoretical inspiration from here:
#   https://hal.inria.fr/inria-00402079/document

from dataclasses import dataclass
from functools import cached_property

import numpy as np
from tqdm import tqdm

from easy_lib.timing import time_func
from procedural_gen.noise.fbm_base import sample


# Smooths out slopes of `terrain` that are too steep. Rough approximation of the
# phenomenon described here: https://en.wikipedia.org/wiki/Angle_of_repose
@time_func
def apply_slippage(terrain, repose_slope, cell_width):
    delta = simple_gradient(terrain) / cell_width
    smoothed = gaussian_blur(terrain, sigma=1.5)
    should_smooth = np.abs(delta) > repose_slope
    result = np.select([np.abs(delta) > repose_slope], [smoothed], terrain)
    return result


# Peforms a gaussian blur of `a`.
@time_func
def gaussian_blur(a, sigma=1.0):
    freqs = tuple(np.fft.fftfreq(n, d=1.0 / n) for n in a.shape)
    freq_radial = np.hypot(*np.meshgrid(*freqs))
    sigma2 = sigma ** 2
    g = lambda x: ((2 * np.pi * sigma2) ** -0.5) * np.exp(-0.5 * (x / sigma) ** 2)
    kernel = g(freq_radial)
    kernel /= kernel.sum()
    return np.fft.ifft2(np.fft.fft2(a) * np.fft.fft2(kernel)).real


# Simple gradient by taking the diff of each cell's horizontal and vertical
# neighbors.
@time_func
def simple_gradient(a):
    dx = 0.5 * (np.roll(a, 1, axis=0) - np.roll(a, -1, axis=0))
    dy = 0.5 * (np.roll(a, 1, axis=1) - np.roll(a, -1, axis=1))
    return 1j * dx + dy


@dataclass
class Params:
    full_width: int = 20
    dim: int = 256

    evaporation_rate: float = 0.0005
    rain_rate: float = .0008

    sediment_capacity_constant = 50.0
    dissolving_rate: float = 0.25
    deposition_rate: float = 0.001

    min_height_delta: float = 0.05
    repose_slope: float = 0.03
    gravity: float = 30.0
    gradient_sigma: float = 0.5

    @cached_property
    def grad_array(self):
        return [np.exp(2j * np.pi * np.random.rand(*self.shape))]

    @property
    def shape(self):
        return (self.dim, self.dim)

    @property
    def cell_width(self):
        return self.full_width / self.dim

    @property
    def cell_area(self):
        return self.cell_width ** 2

    @property
    def cell_area_rain_rate(self):
        return self.rain_rate * self.cell_area


class Terrain:
    def __init__(self, height: np.ndarray):
        self.height = height
        # `sediment` is the amount of suspended "dirt" in the water.
        self.sediment = np.zeros_like(self.height)
        # The amount of water. Responsible for carrying sediment.

        self.water = np.zeros_like(self.height)
        self.water_sed = np.zeros((*self.height.shape, 2))
        self.water_velocity = np.zeros_like(self.height)

    @time_func
    def compute_gradient(self, params: Params):
        # gradient = np.zeros_like(self.height, dtype='complex')
        gradient = simple_gradient(self.height)
        gradient = np.select(
            [np.abs(gradient) < 1e-10],
            [np.exp(2j * np.pi * np.random.rand(*params.shape))],
            gradient
        )
        gradient /= np.abs(gradient)
        return gradient

    # Takes each value of `a` and offsets them by `delta`. Treats each grid point
    # like a unit square.
    @time_func
    def displace(self, a: np.ndarray, delta):
        fns = {
            -1: lambda x: -x,
            0: lambda x: 1 - np.abs(x),
            1: lambda x: x,
        }
        result = np.zeros_like(a)
        for dx in range(-1, 2):
            wx = np.maximum(fns[dx](delta.real), 0.0)
            for dy in range(-1, 2):
                wy = np.maximum(fns[dy](delta.imag), 0.0)
                result += np.roll(np.roll(wx * wy * a, dy, axis=0), dx, axis=1)

        return result

    @time_func
    def single_step(self, params: Params):
        self.add_precipitation(params)
        # Compute the normalized gradient of the terrain height to determine where
        # water and sediment will be moving.
        gradient = self.compute_gradient(params)

        # Compute the difference between teh current height the height offset by
        # `gradient`.
        neighbor_height = sample(self.height, -gradient)
        height_delta = self.height - neighbor_height
        # The sediment capacity represents how much sediment can be suspended in
        # water. If the sediment exceeds the quantity, then it is deposited,
        # otherwise terrain is eroded.
        sediment_capacity = (
                (np.maximum(height_delta, params.min_height_delta) / params.cell_width) * self.water_velocity *
                self.water * params.sediment_capacity_constant)
        deposited_sediment = np.select(
            [
                height_delta < 0,
                self.sediment > sediment_capacity,
            ], [
                np.minimum(height_delta, self.sediment),
                params.deposition_rate * (self.sediment - sediment_capacity),
            ],
            # If sediment <= sediment_capacity
            params.dissolving_rate * (self.sediment - sediment_capacity))
        # Don't erode more sediment than the current terrain height.
        deposited_sediment = np.maximum(-height_delta, deposited_sediment)
        # Update terrain and sediment quantities.
        self.sediment -= deposited_sediment
        self.height += deposited_sediment
        self.sediment = self.displace(self.sediment, gradient)
        self.water = self.displace(self.water, gradient)

        # Smooth out steep slopes.
        # terrain.height = apply_slippage(terrain.height, self.repose_slope, self.cell_width)

        # Update velocity
        self.water_velocity = params.gravity * height_delta / params.cell_width
        # Apply evaporation
        self.water *= 1 - params.evaporation_rate

    @time_func
    def add_precipitation(self, params: Params):
        # self.water += np.ones(self.water.shape) * self.cell_area_rain_rate * .5
        self.water += np.random.rand(*self.water.shape) * params.cell_area_rain_rate

    def simulate(self, params: Params, iterations: int = None):
        if iterations is None:
            iterations = int(1.4 * params.dim)
        for i in tqdm(range(iterations)):
            self.single_step(params)
        return self.height
