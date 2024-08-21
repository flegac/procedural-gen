from abc import ABC

import numpy as np


class PatchTemplate(ABC):
    def get_patch(self, size_px: int) -> np.ndarray:
        ...
