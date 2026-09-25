from collections.abc import Iterator
from math import hypot, atan2, cos, sin, pi
from random import random
from typing import Self


class Vector:
    _EPSILON: int | float = 0.001

    __slots__ = ("_x", "_y")

    def __init__(
            self,
            x: int | float,
            y: int | float,
    ) -> None:
        self._x: int | float = x if abs(x) >= self._EPSILON else 0
        self._y: int | float = y if abs(y) >= self._EPSILON else 0

    @classmethod
    def zero(cls) -> Self:
        return cls(0, 0)

    @classmethod
    def random(cls) -> Self:
        return cls.from_angle(random() * pi * 2)

    @classmethod
    def from_tuple(
            cls,
            vector_tuple: tuple[int | float, int | float],
    ) -> Self:
        return cls(vector_tuple[0], vector_tuple[1])

    @classmethod
    def from_angle(
            cls,
            angle: int | float,
            length: int | float = 1,
    ) -> Self:
        return cls(cos(angle) * length, sin(angle) * length)

    @property
    def x(self) -> int | float:
        return self._x

    @property
    def y(self) -> int | float:
        return self._y

    @property
    def as_tuple(self) -> tuple[int | float, int | float]:
        return self.x, self.y

    @property
    def length(self) -> float:
        return hypot(self.x, self.y)

    @property
    def length_squared(self) -> int | float:
        return self.x * self.x + self.y * self.y

    @property
    def angle(self) -> float:
        return atan2(self.y, self.x)

    def with_x(
            self,
            x: int | float,
    ) -> Self:
        return self.__class__(x, self.y)

    def with_y(
            self,
            y: int | float,
    ) -> Self:
        return self.__class__(self.x, y)

    def with_angle(
            self,
            angle: int | float,
    ) -> Self:
        return self.from_angle(angle, self.length)

    def normalized(self) -> Self:
        length = self.length

        if length == 0:
            return self.zero()

        return self.__class__(self.x / length, self.y / length)

    def dot(
            self,
            other: Self,
    ) -> int | float:
        return self.x * other.x + self.y * other.y

    def cross(
            self,
            other: Self,
    ) -> int | float:
        return self.x * other.y - self.y * other.x

    def distance_to(
            self,
            other: Self,
    ) -> float:
        return (other - self).length

    def distance_squared_to(
            self,
            other: Self
    ) -> int | float:
        return (other - self).length_squared

    def direction_to(
            self,
            other: Self,
    ) -> Self:
        return (other - self).normalized()

    def angle_to(
            self,
            other: Self,
    ) -> float:
        return atan2(self.cross(other), self.dot(other))

    def __add__(
            self,
            other: Self,
    ) -> Self:
        if not isinstance(other, Vector):
            # noinspection PyTypeChecker
            return NotImplemented

        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(
            self,
            other: Self,
    ) -> Self:
        if not isinstance(other, Vector):
            # noinspection PyTypeChecker
            return NotImplemented

        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(
            self,
            other: Self | int | float,
    ) -> Self:
        if isinstance(other, Vector):
            return self.__class__(self.x * other.x, self.y * other.y)

        if isinstance(other, (int, float)):
            return self.__class__(self.x * other, self.y * other)

        # noinspection PyTypeChecker

        return NotImplemented

    def __rmul__(
            self,
            other: int | float,
    ) -> Self:
        return self.__mul__(other)

    def __pos__(self) -> Self:
        return self

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y)

    def __eq__(
            self,
            other: object,
    ) -> bool:
        if not isinstance(other, Vector):
            # noinspection PyTypeChecker
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0

    def __iter__(self) -> Iterator[int | float]:
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> int | float:
        return self.as_tuple[index]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x:.3f}, y={self.y:.3f})"
