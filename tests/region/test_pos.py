from easy_lib.timing import TimingTestCase
from procedural_gen.region.vec import Vec


class TestVec(TimingTestCase):

    def test_init(self):
        pos = Vec.at(2, 3, 4)
        self.assertEqual(pos.vec, [2, 3, 4])
        self.assertEqual(pos.x, 2)
        self.assertEqual(pos.y, 3)
        self.assertEqual(pos.z, 4)

    def test_set_equal(self):
        pos = Vec.at(2, 3, 4)

        pos.x = 6
        pos.y = 7
        pos.z = 8

        self.assertEqual(pos, Vec.at(6, 7, 8))

    def test_operators(self):
        x = Vec.at(1, 2, 3)

        self.assertEqual(x + 3, Vec.at(4, 5, 6))
        self.assertEqual(x + Vec.at(2, 1, 2), Vec.at(3, 3, 5))

        self.assertEqual(x * 3, Vec.at(3, 6, 9))
        self.assertEqual(x * Vec.at(2, 1, 2), Vec.at(2, 2, 6))

        self.assertEqual(x / 2, Vec.at(.5, 1, 1.5))
        self.assertEqual(x / Vec.at(2, 1, 2), Vec.at(.5, 2, 1.5))

    def test_cast(self):
        x = Vec.cast(3)

        self.assertEqual(x, Vec.at(3, 3, 3))
