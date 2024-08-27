from pathlib import Path

from easy_kit.timing import TimingTestCase
from image_io.image_io import ImageIO
from procedural_gen.morphology.morphology import Dilate, Morph, Erode, Opening, Closing

SIZE = 7
STEPS = 1

OUTPUT = Path.cwd() / '_out'


class TestMorphology(TimingTestCase):

    def _apply_op(self, operator: Morph):
        path = Path('height.png')
        buffer = ImageIO.read(path)
        buffer = operator(buffer)
        ImageIO.write(OUTPUT / f'__{operator.__class__.__name__}.png', buffer)

    def test_dilate(self):
        self._apply_op(operator=Dilate.disc(size=SIZE, iterations=STEPS))

    def test_erode(self):
        self._apply_op(operator=Erode.disc(size=SIZE, iterations=STEPS))

    def test_opening(self):
        self._apply_op(operator=Opening.disc(size=SIZE, iterations=STEPS))

    def test_closing(self):
        self._apply_op(operator=Closing.disc(size=SIZE, iterations=STEPS))
