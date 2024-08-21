from pathlib import Path

from loguru import logger

from easy_lib.timing import TimingTestCase
from image_io.buffer_util import BufferUtil
from image_io.image_io import ImageIO
from image_io.resolution import Resolution
from procedural_gen.object_distribution.item_map import ItemMap
from procedural_gen.object_distribution.object_instance import ObjectInstance
from procedural_gen.region.region import Region
from procedural_gen.region.vec import Vec
from procedural_gen.textures.noise.model import NModel
from procedural_gen.textures.noise.seed import NSeed
from procedural_gen.textures.textures import Textures

OUTPUT = Path.cwd() / '_out'


class TestItemMap(TimingTestCase):
    def test_mkp(self):
        n = 200
        size = .025

        buffer = ImageIO.read(OUTPUT / '_raw_mask.png').astype('float')
        buffer = buffer[::, ::, 0]
        buffer = BufferUtil.normalize(buffer)
        # buffer[buffer >= .75] = 0
        # buffer[buffer <= .2] = 0
        # buffer[buffer != 0] = 1
        # buffer = BufferUtil.normalize(buffer)

        # Textures.gray().dump_png('_raw_mask', buffer)
        cache = ItemMap()
        cache.mask.mask[::, ::] = 1
        cache.mask.prepare_map(buffer, treshold=.7, value=0)
        background = cache.mask.mask.copy()

        # bg_path = Textures.colorize((255, 178, 125)).dump_png(OUTPUT/f'_background', background)
        bg_path = Textures.colorize((255, 255, 255)).dump_png(OUTPUT / f'_background', background)
        bg_color = ImageIO.read(bg_path)

        for i in range(4):
            items = cache.place_items(
                template=ObjectInstance(
                    radius=size * .5 ** i
                ),
                n=n * 4 ** i,
            )
            logger.info(f'items: {len(items)}')
            items = Textures.colorize((0, 176, 240)).dump_png(OUTPUT / f'_items_{i}', cache.mask.mask - background)
            foreground = ImageIO.read(items)
            foreground += bg_color
            print(foreground.shape)
            ImageIO.write(OUTPUT / f'_final_{i}.png', foreground)

    def test_item_map(self):
        NModel.clear_cache()
        model = NModel(
            noise=NSeed(seed=2210, roughness=.65),
            region=Region.from_center(Vec(), 2)
        )
        buffer = model.fbm(Resolution.square(128), lod=3)
        Textures.gray().dump_png(OUTPUT / f'_raw_mask', buffer)

        n = 10
        size = .1

        cache = ItemMap()
        cache.mask.prepare_map(buffer, treshold=.0)
        background = cache.mask.mask.copy()

        bg_path = Textures.colorize((255, 178, 125)).dump_png(OUTPUT / f'_background', cache.mask.mask)
        bg_color = ImageIO.read(bg_path)

        for i in range(6):
            items = cache.place_items(
                template=ObjectInstance(
                    radius=size * .5 ** i
                ),
                n=n * 4 ** i,
            )
            logger.info(f'items: {len(items)}')
            items = Textures.colorize((125, 255, 125)).dump_png(OUTPUT / f'_items_{i}', cache.mask.mask - background)
            foreground = ImageIO.read(items)
            foreground += bg_color
            print(foreground.shape)
            ImageIO.write(OUTPUT / f'_final_{i}.png', foreground)
