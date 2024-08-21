from perlin_numpy import generate_fractal_noise_2d

from image_io.buffer_util import BufferUtil
from image_io.resolution import Resolution


def seamless_noise(
        resolution: Resolution,
        octaves: int = 4,
        persistence: float = .5,
        lacunarity: int = 2,
):
    res = 4
    size = lacunarity ** (octaves - 1) * res
    buffer = generate_fractal_noise_2d(
        shape=(size, size),
        res=(res, res),
        persistence=persistence,
        lacunarity=lacunarity,
        octaves=octaves,
        tileable=(True, True)
    )
    buffer = BufferUtil.resize(buffer, resolution, seamless=True)
    return buffer
