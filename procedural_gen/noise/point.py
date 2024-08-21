from typing import NamedTuple, Self


class Point(NamedTuple):
    x: float = 0
    y: float = 0
    z: float = 0

    def __mul__(self, value: float) -> Self:
        return Point(x=self.x * value, y=self.y * value, z=self.z * value)

    def __mod__(self, value: float) -> Self:
        return Point(x=self.x % value, y=self.y % value, z=self.z % value)
