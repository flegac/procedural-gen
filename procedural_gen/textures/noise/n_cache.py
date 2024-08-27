import math
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from tqdm import tqdm

from image_io.image_io import ImageIO
from easy_kit.timing import time_func
from procedural_gen.config import NOISE_CACHE
from image_io.resolution import Resolution
from procedural_gen.textures.noise.seed import NSeed
from procedural_gen.region.region import Region
from procedural_gen.region.vec import Vec

io = ImageIO


@dataclass
class NOffset:
    x: int
    y: int
    lod: int = 1

    @property
    def region(self):
        size = math.pow(2, self.lod)
        return Region.from_center(Vec.at((.5 + self.x) * size, self.y * size), .5 * size)

    @property
    def key_id(self):
        return f'{self.x}x{self.y}/{self.lod}'


@dataclass
class NCache:
    noise: NSeed
    size: int = 128
    root: Path = field(default=NOISE_CACHE)

    def clear_cache(self):
        shutil.rmtree(self.root, ignore_errors=True)
        return self

    def target_path(self, offset: NOffset, ):
        return self.root / f'{self.size}/{offset.key_id}.tif'

    def fbm(self, offset: NOffset, lod: int):
        self.precompute(offset, lod)
        buffer = self.new_buffer()
        for _ in range(lod):
            data = io.read(self.target_path(offset))
            scale_z = self.noise.roughness ** _
            buffer += scale_z * data
        return buffer

    def heighmap(self, region: Region, lod: int):
        raise NotImplementedError

    @time_func
    def precompute(self, offset: NOffset):
        for _ in tqdm(range(offset.lod), f'{self}: precompute'):
            layer = NOffset(offset.x, offset.y, _)
            path = self.target_path(layer)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                continue
            region = layer.region
            data = self.noise.fbm_layer(
                x=region.x.coords(self.size),
                y=region.y.coords(self.size),
                lod=_
            )
            io.write(path, data)

    def new_buffer(self):
        return Resolution.square(self.size).new_buffer()
