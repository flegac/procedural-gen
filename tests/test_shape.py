from pathlib import Path

import numpy as np

from easy_kit.timing import TimingTestCase
from procedural_gen.object_distribution.shape import Shape
from procedural_gen.textures.textures import Textures

OUTPUT = Path.cwd() / '_out'


class TestShape(TimingTestCase):
    def test_circle(self):
        shape = Shape.circle(15)

        Textures.gray().dump_png(OUTPUT / f'circle_{shape.width}x{shape.height}', shape.buffer)

    def test_draw(self):
        buffer = np.zeros((100, 100))
        shape = Shape.circle(15)

        shape2 = Shape.random(10, 15)

        shape2.draw(50, 50, buffer)

        shape.draw(5, 5, buffer)
        shape.draw(30, 30, buffer)
        shape.draw(50, 85, buffer)

        Textures.gray().dump_png(OUTPUT / 'draw', buffer)

    def test_dilate(self):
        # shape = Shape.random(15, 9)
        shape = Shape.circle(10)
        Textures.gray().dump_png(OUTPUT / f'shape_{shape.width}x{shape.height}', shape.buffer)

        dilated = shape.dilated()

        Textures.gray().dump_png(OUTPUT / f'dilated_{dilated.width}x{dilated.height}', dilated.buffer)
