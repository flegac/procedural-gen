import procedural_gen.noise.fbm_base
from easy_lib.timing import TimingTestCase
from procedural_gen.textures.noise.model import NModel
from image_io.resolution import Resolution
from procedural_gen.textures.noise.seed import NSeed
from procedural_gen.region.region import Region
from procedural_gen.region.vec import Vec
from procedural_gen.textures.textures import Textures


class TestNoiseModel(TimingTestCase):

    def test_model_split(self):
        resolution = Resolution.square(256)
        origin = Region()
        texture = Textures.rgb()
        model = NModel(
            noise=NSeed(seed=33),
            region=origin
        )
        lod = 8

        buffer = model.fbm(resolution, lod)
        texture.dump_png(f'{model.region}', buffer)

        for part in model.split(2, 2):
            buffer = procedural_gen.noise.fbm_base.fbm(resolution.raw(), lod)
            texture.dump_png(f'{part.region}', buffer)

    def test_model(self):
        origin = Region.from_center(Vec(), 2)

        NModel.clear_cache()
        model = NModel(
            noise=NSeed(seed=2210, roughness=.65),
            region=origin
        )
        lod = 6
        buffer = model.fbm(Resolution.square(1 + 256), lod)
        # buffer = Rigged().apply_array(buffer)
        Textures.earth().dump_png(f'{model.region}_{lod}', buffer)

        buffer = model.fbm(Resolution.square(1 + 128), lod)
        # buffer = Rigged().apply_array(buffer)
        Textures.gray().dump_png(f'{model.region}_{lod}', buffer)
