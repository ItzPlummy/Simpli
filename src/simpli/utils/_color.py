from typing import Self

from simpli.utils._resolvable import Resolvable, resolve

type _InitColor = Resolvable[int | float] | None


class Color:
    def __init__(
            self,
            red: _InitColor = None,
            green: _InitColor = None,
            blue: _InitColor = None,
            alpha: _InitColor = None,
    ) -> None:
        self._red: Resolvable[int | float] = red if callable(red) else self._resolve_color_float(red or 0)
        self._green: Resolvable[int | float] = green if callable(green) else self._resolve_color_float(green or 0)
        self._blue: Resolvable[int | float] = blue if callable(blue) else self._resolve_color_float(blue or 0)
        self._alpha: Resolvable[int | float] = alpha if callable(alpha) else self._resolve_color_float(1 if alpha is None else alpha)

    @classmethod
    def white(cls) -> Self:
        return cls(1, 1, 1)

    @classmethod
    def black(cls) -> Self:
        return cls(0, 0, 0)

    @classmethod
    def from_tuple(
            cls,
            color_tuple: tuple[_InitColor, _InitColor, _InitColor, _InitColor],
    ) -> Self:
        return cls(color_tuple[0], color_tuple[1], color_tuple[2], color_tuple[3])

    @property
    def red(self) -> int | float:
        return self._resolve_color_float(self._red)

    @property
    def green(self) -> int | float:
        return self._resolve_color_float(self._green)

    @property
    def blue(self) -> int | float:
        return self._resolve_color_float(self._blue)

    @property
    def alpha(self) -> int | float:
        return self._resolve_color_float(self._alpha)

    @property
    def as_tuple(self) -> tuple[int | float, int | float, int | float, int | float]:
        return self.red, self.green, self.blue, self.alpha

    @classmethod
    def _resolve_color_float(
            cls,
            value: Resolvable[int | float],
    ) -> int | float:
        value: int | float = resolve(value)

        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a real number")

        if value < 0 or value > 1:
            raise ValueError("Value must be a real number between 0 and 1")

        return value
