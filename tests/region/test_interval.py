import numpy as np
from numpy.testing import assert_array_equal

from easy_kit.timing import TimingTestCase, time_func
from procedural_gen.region.interval import Interval


class TestInterval(TimingTestCase):
    @time_func
    def test_offset(self):
        interval = Interval(start=-1.3, end=5.7)

        offsets = np.linspace(-12, 27, 123)

        expected = interval.start + offsets * interval.size
        actual = np.array([interval.interpolate(x) for x in offsets])

        assert_array_equal(expected, actual)

    @time_func
    def test_select(self):
        origin = Interval()

        area = Interval.from_center(1 / 2, 1 / 4)

        zoom1 = area.select(origin)
        self.assertEqual(Interval(start=1 / 4, end=3 / 4), zoom1)

        zoom2 = zoom1.select(zoom1)
        self.assertEqual(Interval(start=1 / 4 + 1 / 8, end=3 / 4 - 1 / 8), zoom2)

        zoom3 = zoom2.select(zoom2)
        self.assertEqual(Interval(start=0.46875, end=0.53125), zoom3)

    @time_func
    def test_coords(self):
        actual = Interval.from_center(3, .5).coords(20)
        expected = np.linspace(2.5, 3.5, 20)
        assert_array_equal(expected, actual)

    @time_func
    def test_split(self):
        n = 17
        actual = Interval().split(n)
        print(actual)
        self.assertEqual(n, len(actual))

        expected = [
            Interval(start=i / n, end=(i + 1) / n)
            for i in range(n)
        ]

        for a, e in zip(actual, expected):
            self.assertAlmostEqual(a.start, e.start)
            self.assertAlmostEqual(a.end, e.end)
