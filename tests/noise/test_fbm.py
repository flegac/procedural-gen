import math
from pathlib import Path

import imageio
import numpy as np

from easy_kit.timing import TimingTestCase, time_func, timing
from procedural_gen.noise.fbm_base import fbm, fbm_rigged, sample
from procedural_gen.noise.simulation import Params, Terrain
from procedural_gen.textures.textures import Textures

OUTPUT = Path.cwd() / '_out'
OUTPUT.mkdir(parents=True, exist_ok=True)


class TestIt(TimingTestCase):

    def test_simplest(self):
        size = 512
        radius = size // 2
        height = np.zeros((size, size))

        for i in range(size):
            y = i / (size - 1)
            y = math.sin(y * math.pi * .5)
            for j in range(size):
                x = j / (size - 1)
                x = 1 - math.sin(x * math.pi)

                height[i, j] = 1 * x + 1 * y  # + random.random() * .05

        Textures.gray().dump_png('_biplan', height, root=OUTPUT)

    def test_create(self):
        size = 512
        center = size // 2
        height = np.zeros((size, size))

        def draw(x: int, y: int, radius: int, offset: float = 0., ratio: float = 1., fill: float = None):
            init = height[x, y]
            for i in range(-radius, radius):
                for j in range(-radius, radius):
                    height[y + i, x + j] = (offset * init
                                            + ratio * 4 * (abs(i) / (radius - 1) - .5) * (abs(j) / (radius - 1) - .5))
                    if fill is not None:
                        height[y + i, x + j] = fill

        draw(center, center, center, ratio=-1.)

        other_radius = 40

        draw(256, center, other_radius, ratio=.1)
        draw(size - 256, center, other_radius, ratio=.1)
        draw(center, 256, other_radius, ratio=.1)
        draw(center, size - 256, other_radius, ratio=.1)

        sink_radius = 30
        draw(sink_radius, sink_radius, sink_radius, fill=-2)
        draw(sink_radius, size - sink_radius, sink_radius, fill=-2)
        draw(size - sink_radius, sink_radius, sink_radius, fill=-2)
        draw(size - sink_radius, size - sink_radius, sink_radius, fill=-2)
        draw(center, center, 40, fill=-2)

        Textures.gray().dump_png('_simple', height, root=OUTPUT)

    def test_simulation(self):
        params = Params(
            dim=128,
            dissolving_rate=.001
        )
        height = fbm(params.shape, -2.3, seed=2210)
        Textures.gray().dump_png('_height_origin', height, root=OUTPUT)
        Textures.hill_shaded().dump_png('_texture_origin', height, root=OUTPUT)

        terrain = Terrain(height)
        height = terrain.simulate(params, iterations=params.dim // 1)

        Textures.gray().dump_png(f'_height_{params.dim}', height, root=OUTPUT)
        # Textures.mountains().dump_png('_texture', height, root=OUTPUT)
        Textures.hill_shaded().dump_png('_texture', height, root=OUTPUT)

    @time_func
    def test_fbm(self):
        for size in [512, 1024, 2048, 4096, 8096]:
            with timing(f'fbm_{size}'):
                shape = (size, size)
                Textures.gray().dump_png(
                    f'_fbm_{size}',
                    fbm(shape=shape, seed=2210)
                )

    def test_rigged(self):
        shape = (512, 512)
        result = fbm_rigged(shape)

        Textures.gray().dump_png('_rigged', result)

    def test_domain_warping(self):
        shape = (380, 380)

        with imageio.get_writer('_out.gif', mode='I') as writer:
            for strength in range(50):
                values = fbm(shape, lower=2.0, seed=2210)
                offsets = 10 * strength * (
                        fbm(shape, -2, lower=2, seed=22101) +
                        1j * fbm(shape, -2, lower=2, seed=22102)
                )
                result = sample(values, offsets)

                writer.append_data(Textures.gray().apply(result))

                # Textures.gray().dump_png(f'_warp_final_{strength}', result)
