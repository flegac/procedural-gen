from easy_lib.timing import TimingTestCase, timing
from procedural_gen.textures.noise.seed import NSeed
from procedural_gen.region.interval import Interval


class TestNoise(TimingTestCase):
    def test_fbm_layer(self):
        coords = Interval().coords(32)
        noise = NSeed(seed=22)
        with timing('fbm_layer'):
            res_array = noise.fbm_layer(coords, coords)
