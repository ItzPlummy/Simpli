from random import random, shuffle
from typing import Tuple, Self, List


class Color:
    __slots__ = ("_red", "_green", "_blue", "_alpha")

    def __init__(
            self,
            red: float,
            green: float,
            blue: float,
            alpha: float = 1,
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

        return cls(values[0], values[1], values[2])

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

    def __repr__(self) -> str:
        return f"Color(r={self.red}, g={self.green}, b={self.blue}, a={self.alpha})"
