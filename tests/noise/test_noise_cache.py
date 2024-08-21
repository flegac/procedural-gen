from pathlib import Path

from easy_lib.timing import TimingTestCase
from procedural_gen.textures.noise.n_cache import NCache, NOffset
from procedural_gen.textures.noise.seed import NSeed


class TestNoiseCache(TimingTestCase):
    def test_noise_cache(self):
        cache = NCache(noise=NSeed(seed=22), root=Path.cwd())
        offset = NOffset(0, 0, 5)
        cache.precompute(offset)
        # Textures.gray().dump_png(f'{offset.key_id}', buffer)
