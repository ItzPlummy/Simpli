from dataclasses import dataclass
from random import random, shuffle
from typing import Tuple, Self, List


@dataclass(frozen=True, slots=True)
class Color:
    red: float
    green: float
    blue: float
    alpha: float = 1

    @property
    def as_tuple(self) -> Tuple[float, float, float, float]:
        return self.red, self.green, self.blue, self.alpha

    @property
    def as_int_tuple(self) -> Tuple[int, int, int, int]:
        return int(self.red * 255), int(self.green * 255), int(self.blue * 255), int(self.alpha * 255)

    @classmethod
    def random(cls) -> Self:
        values: List[float] = [0, random(), 1]
        shuffle(values)
        return cls(values[0], values[1], values[2])

    @classmethod
    def random_bright(cls) -> Self:
        color: Self = cls.random()
        return cls(
            color.red + (1 - color.red) / 2,
            color.green + (1 - color.green) / 2,
            color.blue + (1 - color.blue) / 2,
        )

    @classmethod
    def random_dark(cls) -> Self:
        color: Self = cls.random()
        return cls(
            color.red / 2,
            color.green / 2,
            color.blue / 2,
        )

    @classmethod
    def black(cls) -> Self:
        return cls(0, 0, 0)

    @classmethod
    def white(cls) -> Self:
        return cls(1, 1, 1)

    @classmethod
    def shadow(cls) -> Self:
        return cls(0.15, 0.15, 0.15, 0.1)

    def __repr__(self) -> str:
        return f"Color(r={self.red}, g={self.green}, b={self.blue}, a={self.alpha})"
