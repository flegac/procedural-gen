import numpy as np
from numpy.testing import assert_array_equal

from easy_lib.timing import TimingTestCase
from procedural_gen.region.vec import Vec
from procedural_gen.region.region import Region


class TestRegion(TimingTestCase):
    def test_offset(self):
        expected = Vec(vec=[0.25, 0.34, 0])
        self.assertEqual(expected, Region().interpolate(Vec.at(.25, .34)))

    def test_select(self):
        origin = Region()
        area = Region.from_center(Vec.at(.5, .5), 1)

        selection = area.select(origin)
        self.assertEqual(selection, area)

    def test_coords(self):
        x, y, z = Region().coords(2, 3, 2)
        # print(f'zz=np.{repr(z)}')
        xx = np.array([[[0., 0.],
                        [1., 1.]],

                       [[0., 0.],
                        [1., 1.]],

                       [[0., 0.],
                        [1., 1.]]])
        yy = np.array([[[0., 0.],
                        [0., 0.]],

                       [[0.5, 0.5],
                        [0.5, 0.5]],

                       [[1., 1.],
                        [1., 1.]]])
        zz = np.array([[[0., 1.],
                        [0., 1.]],

                       [[0., 1.],
                        [0., 1.]],

                       [[0., 1.],
                        [0., 1.]]])
        assert_array_equal(x, xx)
        assert_array_equal(y, yy)
        assert_array_equal(z, zz)

    def test_split(self):
        n = 2
        origin = Region()

        actual = origin.split(n, n)

        print(actual)
