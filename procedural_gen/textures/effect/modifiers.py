from abc import ABC, abstractmethod
from enum import Enum

import numpy as np


class NoiseModifier(ABC):

    def apply_array(self, buffer: np.ndarray):
        mapper = np.vectorize(self.apply)
        return mapper(buffer)

    @abstractmethod
    def apply(self, value: float) -> float:
        ...

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return repr(self)


class Identity(NoiseModifier):

    def apply(self, value: float) -> float:
        return value


class Rigged(NoiseModifier):

    def apply(self, value: float) -> float:
        return 1 - abs(value)


class Wood(NoiseModifier):
    def apply(self, value: float):
        n = 5.
        k = 1 / n
        return n * (value % k)


class Modifiers(Enum):
    Identity = Identity
    Rigged = Rigged
    Wood = Wood
