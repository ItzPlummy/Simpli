from dataclasses import dataclass
from math import pi, cos, sin, sqrt
from random import random
from typing import Self, Tuple


@dataclass(frozen=True, slots=True)
class Vector:
    x: float
    y: float

    @property
    def length(self) -> float:
        return sqrt(self.length_squared)

    @property
    def length_squared(self) -> float:
        return self.x ** 2 + self.y ** 2

    @property
    def normalized(self) -> Self:
        length = self.length

        if length == 0:
            return Vector(0.0, 0.0)

        return Vector(self.x / length, self.y / length)

    @property
    def as_tuple(self) -> Tuple[float, float]:
        return self.x, self.y

    @classmethod
    def zero(cls) -> Self:
        return Vector(0, 0)

    @classmethod
    def random(cls) -> Self:
        angle: float = 2 * pi * random()

        return Vector(cos(angle), sin(angle))

    @classmethod
    def from_tuple(
            cls,
            vector_tuple: Tuple[float, float],
    ) -> Self:
        return cls(*vector_tuple)

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"

    def __add__(
            self,
            other: Self,
    ) -> Self:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(
            self,
            other: Self,
    ) -> Self:
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(
            self,
            value: float
    ) -> Self:
        return Vector(self.x * value, self.y * value)

    def __rmul__(
            self,
            value: float
    ) -> Self:
        return self.__mul__(value)

    def __eq__(
            self,
            other: Self
    ) -> bool:
        return self.x == other.x and self.y == other.y

    def __neg__(self) -> Self:
        return Vector(-self.x, -self.y)

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def dot(
            self,
            other: Self
    ) -> float:
        return self.x * other.x + self.y * other.y
