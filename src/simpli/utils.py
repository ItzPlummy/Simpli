from math import pi, cos, sin, sqrt
from random import random, shuffle
from typing import Self, Tuple, List


class Vector:
    __slots__ = ("_x", "_y")

    def __init__(
            self,
            x: float,
            y: float,
    ) -> None:
        self._x = float(x)
        self._y = float(y)

        if abs(self._x) < 0.0001:
            self._x = float(0)
        if abs(self._y) < 0.0001:
            self._y = float(0)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        if abs(value) < 0.0001:
            self._x = float(0)
        else:
            self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        if abs(value) < 0.0001:
            self._y = float(0)
        else:
            self._y = float(value)

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
        return self._x, self._y

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

    def copy(self) -> Self:
        return Vector(self._x, self._y)


class Color:
    __slots__ = ("_red", "_green", "_blue", "_alpha")

    def __init__(
            self,
            red: float,
            green: float,
            blue: float,
            alpha: float,
    ) -> None:
        self._red = float(red)
        self._green = float(green)
        self._blue = float(blue)
        self._alpha = float(alpha)

    @property
    def red(self) -> float:
        return self._red

    @red.setter
    def red(self, value: float) -> None:
        self._red = float(value)

    @property
    def green(self) -> float:
        return self._green

    @green.setter
    def green(self, value: float) -> None:
        self._green = float(value)

    @property
    def blue(self) -> float:
        return self._blue

    @blue.setter
    def blue(self, value: float) -> None:
        self._blue = float(value)

    @property
    def alpha(self) -> float:
        return self._alpha

    @alpha.setter
    def alpha(self, value: float) -> None:
        self._alpha = float(value)

    @property
    def as_tuple(self) -> Tuple[float, float, float, float]:
        return self._red, self._green, self._blue, self._alpha

    @property
    def as_int_tuple(self) -> Tuple[int, int, int, int]:
        return int(self._red * 255), int(self._green * 255), int(self._blue * 255), int(self._alpha * 255)

    @classmethod
    def random(cls) -> Self:
        values: List[float] = [0, random(), 1]
        shuffle(values)

        return cls(values[0], values[1], values[2], 1)

    @classmethod
    def random_bright(cls) -> Self:
        color: Self = cls.random()

        color.red += (1 - color.red) / 2
        color.green += (1 - color.green) / 2
        color.blue += (1 - color.blue) / 2

        return color

    @classmethod
    def random_dark(cls) -> Self:
        color: Self = cls.random()

        color.red /= 2
        color.green /= 2
        color.blue /= 2

        return color

    @classmethod
    def shadow(cls) -> Self:
        return cls(0.15, 0.15, 0.15, 0.1)

    def copy(self) -> Self:
        return Color(self._red, self._green, self._blue, self._alpha)
