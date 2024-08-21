import numpy as np

from image_io.resolution import Resolution
from procedural_gen.textures.textures import Textures
from procedural_gen.textures.noise.seamless_noise import seamless_noise

if __name__ == '__main__':
    np.random.seed(2210)
    buffer = seamless_noise(
        resolution=Resolution.square(32 + 1),
        lacunarity=2,
        octaves=8,
        persistence=.65,
    )
    Textures.gray().dump_png(f'height', buffer)
