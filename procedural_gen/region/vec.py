import math
from numbers import Number
from random import random
from typing import Self, Any, Sequence

from pydantic import Field

from easy_config.my_model import MyModel

EPSILON = .001


class Vec(MyModel):
    vec: list[float | None] = Field(default_factory=lambda: [0, 0, 0])

    @staticmethod
    def cast(item: Any):
        if item is None:
            return Vec.at(None, None, None)
        if isinstance(item, Vec):
            return item
        if isinstance(item, Number):
            return Vec.at(item, item, item)

        loaders = [
            lambda: (item.x, item.y, item.z),
            lambda: (item.get_x(), item.get_y(), item.get_z()),
        ]
        for loader in loaders:
            try:
                return Vec.at(*loader())
            except:
                continue
        raise ValueError(f'could not cast vector: {type(item)}')

    @staticmethod
    def interpolate(start: 'Vec', target: 'Vec', x: float):
        if target is None:
            return start
        if start is None:
            start = Vec()
        return start * (1 - x) + target * x

    @staticmethod
    def rand_direction(length: float = 1):
        res = Vec.cast(1)
        while res.length() > 1:
            res = 2 * Vec.at(random() - .5, random() - .5, random() - .5)
        return res.normalized() * length

    @staticmethod
    def at(x: float = 0, y: float = 0, z: float = 0):
        return Vec(vec=[x, y, z])

    @staticmethod
    def mass_center(vecs: list['Vec']):
        center = Vec()
        for _ in vecs:
            center += _
        return center / len(vecs)

    @staticmethod
    def bbox(vecs: list['Vec']):
        a = Vec()
        b = Vec()
        for _ in vecs:
            a.x = min(a.x, _.x)
            a.y = min(a.y, _.y)
            a.z = min(a.z, _.z)
            b.x = max(b.x, _.x)
            b.y = max(b.y, _.y)
            b.z = max(b.z, _.z)

        center = (b + a) * .5
        size = b - a
        return center, size

    @property
    def invert_x(self):
        return Vec.at(-self.x, self.y, self.z)

    @property
    def invert_y(self):
        return Vec.at(self.x, -self.y, self.z)

    @property
    def invert_z(self):
        return Vec.at(self.x, self.y, -self.z)

    def explode(self, xyz: Self, symmetric: bool = True):
        dirs = [
            xyz.x * Vec.x_axis(),
            xyz.y * Vec.y_axis(),
            xyz.z * Vec.z_axis(),
        ]
        if symmetric:
            dirs.extend([
                -xyz.x * Vec.x_axis(),
                -xyz.y * Vec.y_axis(),
                -xyz.z * Vec.z_axis(),
            ])

        return [
            self + dir
            for dir in dirs
            if dir.length() != 0
        ]

    @staticmethod
    def x_axis():
        return Vec.at(1, 0, 0)

    @staticmethod
    def y_axis():
        return Vec.at(0, 1, 0)

    @staticmethod
    def z_axis():
        return Vec.at(0, 0, 1)

    def dist(self, other: Self):
        return (self - other).length()

    def nearest(self, vecs: Sequence[Self]) -> Self:
        res = vecs[0]
        d = self.dist(res)
        for _ in vecs[1:]:
            if d == 0:
                return res
            dd = self.dist(_)
            if dd < d:
                d = dd
                res = _
        return res

    def farthest(self, vecs: list[Self]):
        res = vecs[0]
        d = self.dist(res)
        for _ in vecs[1:]:
            dd = self.dist(_)
            if dd > d:
                d = dd
                res = _
        return res

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value: float):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value: float):
        self[1] = value

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value: float):
        self[2] = value

    def length(self):
        return math.sqrt(self.dot(self))

    def normalized(self, length: float = 1):
        return self * (length / self.length())

    def cross(self, o: Self):
        return Vec.at(
            x=self.y * o.z - self.z * o.y,
            y=self.z * o.x - self.x * o.z,
            z=self.x * o.y - self.y * o.x,
        )

    def dot(self, o: Self):
        return self.x * o.x + self.y * o.y + self.z * o.z

    def __iter__(self):
        return iter(self.vec)

    def __getitem__(self, item: int):
        return self.vec[item]

    def __setitem__(self, key: int, value: float):
        self.vec[key] = value

    def __add__(self, other: Self | Number):
        other = Vec.cast(other)
        return Vec.at(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: Self | Number):
        other = Vec.cast(other)
        return Vec.at(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, other: Self | Number):
        other = Vec.cast(other)
        return Vec.at(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
        )

    def __truediv__(self, other: Self | Number):
        other = Vec.cast(other)
        return Vec.at(
            self.x / other.x,
            self.y / other.y,
            self.z / other.z,
        )

    def __rmul__(self, other):
        return self * other

    def __radd__(self, other):
        return self * other

    def __rsub__(self, other):
        return -self + other

    def __neg__(self):
        return Vec.at(-self.x, -self.y, -self.z)

    def __eq__(self, other: Self):
        if not isinstance(other, Vec):
            raise ValueError(f'{type(other)}')
        return self.dist(other) <= EPSILON

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        # return f'({self.x:.3E},{self.y:.3E},{self.z:.3E})'
        return f'({self.x:.2f},{self.y:.2f},{self.z:.2f})'

    def __str__(self):
        return repr(self)
