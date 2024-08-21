import math
import random
from typing import Callable

import numpy as np
from tqdm import tqdm

from procedural_gen.textures.effect.patch_template import PatchTemplate

BlendFunc = Callable[[np.ndarray, np.ndarray], np.ndarray]


class Patcher:
    def __init__(self, seed: int, template: PatchTemplate, blend_func: BlendFunc = np.add):
        self.seed = seed
        self.template = template
        self.blend = blend_func

    def apply_many(self, target: np.ndarray, items: int):
        if target.ndim == 2:
            target = target[..., np.newaxis]

        random.seed(self.seed)
        for i in tqdm(range(items), 'Patcher.apply_many'):
            self.patch_at(
                x=random.random(),
                y=random.random(),
                radius=.01 + random.betavariate(alpha=.9, beta=1.5) * .05,
                target=target
            )

    def patch_at(self, x: float, y: float, radius: float, target: np.ndarray):
        resolution = min(target.shape[:2])
        radius_px = math.ceil(radius * resolution)
        size_px = 2 * radius_px

        try:
            patch = self.template.get_patch(size_px) * radius
            if patch.ndim == 2:
                patch = patch[..., np.newaxis]

            x1 = int(x * resolution) - radius_px
            y1 = int(y * resolution) - radius_px
            dx1 = max(0, -x1)
            dx2 = max(0, (x1 + size_px) - (target.shape[1] - 1))
            dy1 = max(0, -y1)
            dy2 = max(0, (y1 + size_px) - (target.shape[0] - 1))

            patch = patch[dy1:size_px - dy2, dx1:size_px - dx2]
            patched_target = target[y1 + dy1:y1 + size_px - dy2, x1 + dx1:x1 + size_px - dx2]
            patched_target[...] = self.blend(patched_target, patch)

        except Exception as e:
            print(f'error with crater at {x:.2f}, {y:.2f}: {e}')
        return target
