import shutil
from dataclasses import dataclass, field

from numpy.testing import assert_array_equal
from tqdm import tqdm

from image_io.image_io import ImageIO
from easy_kit.timing import time_func
from procedural_gen.config import NOISE_CACHE
from image_io.resolution import Resolution
from procedural_gen.textures.noise.seed import NSeed
from procedural_gen.region.region import Region

io = ImageIO


@dataclass
class NModel:
    noise: NSeed
    region: Region = field(default_factory=lambda: Region())

    def split(self, width: int, height: int):
        return [
            NModel(noise=self.noise, region=region)
            for region in self.region.split(width, height)
        ]

    def cache_path(self, resolution: Resolution, lod: int):
        return NOISE_CACHE / f'{self.noise}/{self.region}/{resolution}/{lod}.tif'

    @staticmethod
    def clear_cache():
        shutil.rmtree(NOISE_CACHE, ignore_errors=True)

    def fbm(self, resolution: Resolution, lod: int):
        self.precompute(resolution, lod)
        buffer = resolution.new_buffer()
        for _ in range(lod):
            data = io.read(self.cache_path(resolution, _))
            scale_z = self.noise.roughness ** _
            buffer += scale_z * data
        return buffer

    @time_func
    def precompute(self, resolution: Resolution, lod: int):
        for _ in tqdm(range(lod), f'{self}: precompute'):
            self.precompute_layer(resolution, _)

    def precompute_layer(self, resolution: Resolution, lod: int):
        path = self.cache_path(resolution, lod)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            return
        data = self.noise.fbm_layer(
            x=self.region.x.coords(resolution.width),
            y=self.region.y.coords(resolution.height),
            lod=lod
        )
        io.write(path, data)
        data2 = io.read(path)
        assert_array_equal(data, data2)

    def __repr__(self):
        return f'{self.noise}_{self.region}'

    def __str__(self):
        return repr(self)
