from dataclasses import dataclass
from functools import cached_property

import numpy as np
from opensimplex import OpenSimplex

from easy_lib.timing import time_func


@dataclass
class NSeed:
    seed: int = None
    roughness: float = .5  # per octave amplitude multiplier
    lacunarity: float = 2.0  # per octave frequency multiplier

    @cached_property
    def simplex(self):
        return OpenSimplex(self.seed)

    @time_func
    def fbm_layer(self, x: np.ndarray, y: np.ndarray, lod: int = 0):
        scale_xy = self.lacunarity ** lod
        scale_z = self.roughness ** lod
        scale_z = 1.
        return scale_z * self.simplex.noise2array(y * scale_xy, x * scale_xy)

    def __repr__(self):
        return f'{self.seed}_rough{self.roughness}_factor{self.lacunarity}'

    def __str__(self):
        return repr(self)
