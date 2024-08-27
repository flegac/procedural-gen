from pathlib import Path

import imageio
import numpy as np

from easy_kit.timing import time_func


@time_func
def normalize(x, bounds=(0, 1)):
    return np.interp(x, (x.min(), x.max()), bounds)


@time_func
def lerp(x, y, a):
    return (1.0 - a) * x + a * y


@time_func
def sample(a, offset):
    shape = np.array(a.shape)
    delta = np.array((offset.real, offset.imag))
    coords = np.array(np.meshgrid(*map(range, shape))) - delta

    lower_coords = np.floor(coords).astype(int)
    upper_coords = lower_coords + 1
    coord_offsets = coords - lower_coords
    lower_coords %= shape[:, np.newaxis, np.newaxis]
    upper_coords %= shape[:, np.newaxis, np.newaxis]

    result = lerp(lerp(a[lower_coords[1], lower_coords[0]],
                       a[lower_coords[1], upper_coords[0]],
                       coord_offsets[0]),
                  lerp(a[upper_coords[1], lower_coords[0]],
                       a[upper_coords[1], upper_coords[0]],
                       coord_offsets[0]),
                  coord_offsets[1])
    return result


@time_func
def fbm(shape, p=-2, lower=-np.inf, upper=np.inf, seed: int = None):
    if seed is not None:
        np.random.seed(seed)
    freqs = tuple(np.fft.fftfreq(n, d=1.0 / n) for n in shape)
    freq_radial = np.hypot(*np.meshgrid(*freqs))
    envelope = (np.power(freq_radial, p, where=freq_radial != 0) * (freq_radial > lower) * (freq_radial < upper))
    envelope[0][0] = 0.0
    phase_noise = np.exp(2j * np.pi * np.random.rand(*shape))
    return normalize(np.real(np.fft.ifft2(np.fft.fft2(phase_noise) * envelope)))


def make_gif(targets: list[Path], output_path: Path):
    with imageio.get_writer(output_path, mode='I') as writer:
        for filename in targets:
            image = imageio.imread(filename)
            writer.append_data(image)


@time_func
def fbm_rigged(shape: tuple[int, int], seed: int = None):
    values = np.zeros(shape)
    for p in range(0, 10):
        a = 2 ** p
        values += np.abs(fbm(shape, -2, lower=a, upper=(2 * a), seed=seed) - 0.5) / a
    result = np.power((1.0 - normalize(values)), 2)
    return result


