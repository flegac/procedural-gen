from dataclasses import field, dataclass
from pathlib import Path
from typing import List

import numpy as np
from scipy import interpolate

from easy_lib.timing import time_func
from image_io.buffer_util import BufferUtil
from image_io.image_io import ImageIO

type Color = tuple[int, int, int]

io = ImageIO


@dataclass
class ColorTreshold:
    color: Color
    treshold: float = None

    @staticmethod
    def rgb(r: int, g: int, b: int, treshold: float = None):
        return ColorTreshold(color=(r, g, b), treshold=treshold)

    @staticmethod
    def rgb_float(r: float, g: float, b: float, treshold: float = None):
        return ColorTreshold.rgb(int(255 * r), int(255 * g), int(255 * b), treshold)


rgb = ColorTreshold.rgb
rgb_float = ColorTreshold.rgb_float


@dataclass
class ColorRamp:
    # https://www.google.com/search?channel=fs&client=ubuntu&q=color+picker
    name: str
    colors: List[ColorTreshold] = field(default_factory=lambda: [
        rgb(0, 0, 0, 0),
        rgb(255, 255, 255, 1)
    ])

    def dump_png(self, name: str, heatmap: np.ndarray, root: Path = None):
        path = Path(f'{name}.png')
        if root is not None:
            path = root / path
        heatmap = self.apply(heatmap.copy())
        io.write(path, heatmap)
        return path

    @time_func
    def apply(self, heatmap: np.ndarray):
        heatmap = BufferUtil.normalize(heatmap)
        x = np.linspace(heatmap.min(), heatmap.max(), len(self.colors))
        for i, color in enumerate(self.colors):
            if color.treshold is not None:
                x[i] = color.treshold

        f = interpolate.interp1d(
            x=x,
            y=np.array([c.color for c in self.colors]),
            axis=0
        )
        texture = f(heatmap)
        return texture.astype('uint8')
