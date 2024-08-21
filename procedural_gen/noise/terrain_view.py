from functools import cached_property
from pathlib import Path

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

ROOT = Path('C:/Users\Flo\Documents/workspace/sandbox-3d/docs/assets')


class Light:
    def __init__(
            self,
            pos: tuple[float, float, float],
            color: tuple[float, float, float] = (1, 1, 1, 1)
    ):
        self.pos = pos
        self.color = color

    def apply(self, render):
        plight = PointLight('plight')
        plight.setColor(self.color)
        plnp = render.attachNewNode(plight)
        plnp.setPos(self.pos)
        render.setLight(plnp)


class Terrain:
    def __init__(self, height_path: Path, texture_path: Path):
        self.height_path = height_path
        self.texture_path = texture_path
        self.terrain = GeoMipTerrain("terrain")
        self.scaling = (1, 1, 100 * self.texture_size[0]/512)

    @cached_property
    def height_image(self):
        return PNMImage(Filename(self.height_path))

    @property
    def texture_size(self):
        return self.height_image.getXSize(), self.height_image.getYSize()

    def apply(self, render):
        size = self.texture_size[0]
        half_size = size // 2

        self.terrain.setHeightfield(self.height_path)

        # Applique une texture
        if self.texture_path:
            tex = loader.loadTexture(self.texture_path)
            self.terrain.getRoot().setTexture(tex, 1)
            self.terrain.getRoot().setTwoSided(True)

        terrain_offset = (-half_size, -half_size, 0)
        self.terrain.getRoot().setPos(terrain_offset)
        # Attache le terrain au render
        self.terrain.getRoot().reparentTo(render)
        # Positionne et modifie l'échelle du terrain
        self.terrain.getRoot().setScale(self.scaling)
        # Génère le terrain
        self.terrain.setBruteforce(True)
        self.terrain.generate()


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        root = Path('C:/Users\Flo\Documents/workspace/procedural-gen/tests/noise/_out')

        terrain = Terrain(
            height_path=root / '_height.png',
            texture_path=root / '_texture.png',
            # height_path=root / '_height_origin.png',
            # texture_path=root / '_texture_origin.png',
        )

        size = terrain.texture_size[0]

        self.light = Light(pos=(25, 25, size))
        self.set_background_color((.5, .75, 1.))

        cam_pos = (0, -1. * size, .75 * size)
        cam_lookat = (0, 0, 0)
        self.cam.setPos(cam_pos)
        self.cam.lookAt(cam_lookat)

        terrain.apply(render)

        self.light.apply(render)


if __name__ == '__main__':
    MyApp().run()
