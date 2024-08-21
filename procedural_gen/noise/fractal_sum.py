from typing import Callable


class FractalSum[P]:
    def __init__(self, noise: Callable[[P], float]):
        self.noise = noise

    def fbm(self, layers: int, lacunarity: float = 2, power: float = .5):
        def compute(point: P):
            value = 0
            for i in range(layers):
                frequency = lacunarity ** i
                amplitude = power ** i
                value += self.noise(point * frequency) * amplitude
            return value

        return compute
