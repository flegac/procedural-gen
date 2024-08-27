import imageio
import numpy as np
from scipy.interpolate import griddata

from easy_kit.timing import TimingTestCase, time_func
from procedural_gen.noise.fbm_base import sample, fbm, fbm_rigged
from procedural_gen.noise.interpolators import Interpolators
from procedural_gen.textures.textures import Textures


class GradientNoise:
    def __init__(self, grid_size: int = 16, seed: int = None):
        np.random.seed(seed)

        angles = np.random.random((grid_size * grid_size)) * 2 * np.pi
        self.gradients = np.column_stack((np.cos(angles), np.sin(angles)))

        # self.gradients = np.random.random((grid_size * grid_size, 2))
        # self.gradients = self.gradients / np.sqrt(np.sum(self.gradients ** 2))

        self.grid_size = grid_size
        xx, yy = np.meshgrid(
            np.linspace(0, 1, self.grid_size),
            np.linspace(0, 1, self.grid_size)
        )
        self.points = (xx.flatten(), yy.flatten())

    @time_func
    def noise2d(self, shape: tuple[int, int]):
        grid_x, grid_y = np.meshgrid(
            np.linspace(0, 1, shape[0], endpoint=False),
            np.linspace(0, 1, shape[1], endpoint=False)
        )

        dx0, x0 = np.modf(grid_x * self.grid_size)
        dy0, y0 = np.modf(grid_y * self.grid_size)
        dx1 = 1 - dx0
        dy1 = 1 - dy0

        d00 = np.dstack((dx0, dy0))
        d01 = np.dstack((dx0, dy1))
        d10 = np.dstack((dx1, dy0))
        d11 = np.dstack((dx1, dy1))

        x0 = x0.astype(int)
        y0 = y0.astype(int)
        x1 = (x0 + 1) % self.grid_size
        y1 = (y0 + 1) % self.grid_size

        x0 = x0 / self.grid_size
        y0 = y0 / self.grid_size
        x1 = x1 / self.grid_size
        y1 = y1 / self.grid_size

        g00 = griddata(self.points, self.gradients, (x0, y0), method='cubic', rescale=True)[:, :, :2]
        g01 = griddata(self.points, self.gradients, (x0, y1), method='cubic', rescale=True)[:, :, :2]
        g10 = griddata(self.points, self.gradients, (x1, y0), method='cubic', rescale=True)[:, :, :2]
        g11 = griddata(self.points, self.gradients, (x1, y1), method='cubic', rescale=True)[:, :, :2]

        p00 = np.sum(g00 * d00, axis=2)
        p01 = np.sum(g01 * d01, axis=2)
        p10 = np.sum(g10 * d10, axis=2)
        p11 = np.sum(g11 * d11, axis=2)

        x = dx0
        y = dy0

        inter = Interpolators.poly_6x5_15x4_10x3
        x = inter.apply(x)
        y = inter.apply(y)

        i1 = p00 * (1 - x) + p10 * x
        i2 = p01 * (1 - x) + p11 * x
        res = i1 * (1 - y) + i2 * y

        Textures.gray().dump_png('_dx0', dx0)
        Textures.gray().dump_png('_dx1', dx1)
        Textures.gray().dump_png('_dy0', dy0)
        Textures.gray().dump_png('_dy1', dy1)
        #
        Textures.gray().dump_png('_gx00', g00[:, :, 0])
        Textures.gray().dump_png('_gx01', g01[:, :, 0])
        Textures.gray().dump_png('_gx10', g10[:, :, 0])
        Textures.gray().dump_png('_gx11', g11[:, :, 0])
        #
        Textures.gray().dump_png('_gy00', g00[:, :, 1])
        Textures.gray().dump_png('_gy01', g01[:, :, 1])
        Textures.gray().dump_png('_gy10', g10[:, :, 1])
        Textures.gray().dump_png('_gy11', g11[:, :, 1])
        #

        Textures.gray().dump_png('_x', x)

        Textures.gray().dump_png('_p00', p00)
        Textures.gray().dump_png('_p01', p01)
        Textures.gray().dump_png('_p10', p10)
        Textures.gray().dump_png('_p11', p11)
        #
        Textures.gray().dump_png('_i1', i1)
        Textures.gray().dump_png('_i2', i2)
        Textures.gray().dump_png('_res', res)

        return res


class TestIt(TimingTestCase):

    def test_fbm(self):
        shape = (512, 512)
        for idx, p in enumerate(np.linspace(0, 3, 30)):
            Textures.gray().dump_png(
                f'_aaaa_{idx}',
                fbm(shape=shape, p=-p, seed=2210)
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

    def test_it(self):
        shape = (256, 256)
        noise = GradientNoise(grid_size=8)
        data = noise.noise2d(shape)

        Textures.gray().dump_png('_data', data)
