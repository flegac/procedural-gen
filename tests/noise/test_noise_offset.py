from easy_kit.timing import TimingTestCase
from procedural_gen.textures.noise.n_cache import NOffset
from procedural_gen.region.interval import Interval


class TestNoiseOffset(TimingTestCase):
    def test_offset(self):
        actual = [
            NOffset(x=i, y=0).region.x
            for i in range(-3, 3)
        ]
        expected = [
            Interval.from_center(i - 2, .5)
            for i in range(5)
        ]
        self.assertListEqual(expected, actual)

    def test_offset_scaling(self):
        actual = [
            NOffset(x=i, y=0, lod=-8).region.x
            for i in range(-3, 3)
        ]
        print(actual)
