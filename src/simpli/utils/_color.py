import colorsys
import random
from typing import Self


class Color:
    __slots__ = ("_red", "_green", "_blue", "_alpha")

    def __init__(
            self,
            red: int | float | None = None,
            green: int | float | None = None,
            blue: int | float | None = None,
            alpha: int | float | None = None,
    ) -> None:
        self._red: int | float = self._validate_color_float(red if red is not None else 0)
        self._green: int | float = self._validate_color_float(green if green is not None else 0)
        self._blue: int | float = self._validate_color_float(blue if blue is not None else 0)
        self._alpha: int | float = self._validate_color_float(alpha if alpha is not None else 1)

    @classmethod
    def white(cls) -> Self:
        return cls(1, 1, 1)

    @classmethod
    def black(cls) -> Self:
        return cls(0, 0, 0)

    @classmethod
    def oat(cls) -> Self:
        return cls(0.975, 0.945, 0.88)

    @classmethod
    def random(cls) -> Self:
        return cls._random_with_lightness(0.5)

    @classmethod
    def random_light(cls) -> Self:
        return cls._random_with_lightness(0.75)

    @classmethod
    def random_dark(cls) -> Self:
        return cls._random_with_lightness(0.25)

    @classmethod
    def from_tuple(
            cls,
            color_tuple: tuple[int | float | None, int | float | None, int | float | None, int | float | None],
    ) -> Self:
        return cls(color_tuple[0], color_tuple[1], color_tuple[2], color_tuple[3])

    @classmethod
    def from_hex(
            cls,
            hex_string: str,
    ) -> Self:
        digits = hex_string.removeprefix("#")

        if len(digits) in (3, 4):
            digits = "".join(digit * 2 for digit in digits)

        if len(digits) == 6:
            digits += "ff"

        if len(digits) != 8:
            raise ValueError("Hex string must have 3, 4, 6 or 8 digits")

        try:
            channels = [int(digits[i:i + 2], 16) / 255 for i in range(0, 8, 2)]
        except ValueError:
            raise ValueError(f"Invalid hex string: {hex_string!r}") from None

        return cls(*channels)

    @classmethod
    def from_hsv(
            cls,
            hue: int | float,
            saturation: int | float,
            value: int | float,
            alpha: int | float | None = None,
    ) -> Self:
        red, green, blue = colorsys.hsv_to_rgb(
            cls._validate_color_float(hue),
            cls._validate_color_float(saturation),
            cls._validate_color_float(value),
        )
        return cls(red, green, blue, alpha)

    @property
    def red(self) -> int | float:
        return self._red

    @property
    def green(self) -> int | float:
        return self._green

    @property
    def blue(self) -> int | float:
        return self._blue

    @property
    def alpha(self) -> int | float:
        return self._alpha

    @property
    def hue(self) -> float:
        return self.as_hsv_tuple[0]

    @property
    def saturation(self) -> float:
        return self.as_hsv_tuple[1]

    @property
    def value(self) -> float:
        return self.as_hsv_tuple[2]

    @property
    def as_tuple(self) -> tuple[int | float, int | float, int | float, int | float]:
        return self.red, self.green, self.blue, self.alpha

    @property
    def as_hsv_tuple(self) -> tuple[int | float, int | float, int | float]:
        return colorsys.rgb_to_hsv(self.red, self.green, self.blue)

    def as_hex(
            self,
            include_alpha: bool = True,
    ) -> str:
        channels = self.as_tuple if include_alpha else self.as_tuple[:3]
        return "#" + "".join(f"{round(channel * 255):02x}" for channel in channels)

    def with_rgba(
            self,
            *,
            red: int | float | None = None,
            green: int | float | None = None,
            blue: int | float | None = None,
            alpha: int | float | None = None,
    ) -> Self:
        return self.__class__(
            self.red if red is None else red,
            self.green if green is None else green,
            self.blue if blue is None else blue,
            self.alpha if alpha is None else alpha,
        )

    def with_red(self, red: int | float) -> Self:
        return self.with_rgba(red=red)

    def with_green(self, green: int | float) -> Self:
        return self.with_rgba(green=green)

    def with_blue(self, blue: int | float) -> Self:
        return self.with_rgba(blue=blue)

    def with_alpha(self, alpha: int | float) -> Self:
        return self.with_rgba(alpha=alpha)

    def with_hsv(
            self,
            hue: int | float | None = None,
            saturation: int | float | None = None,
            value: int | float | None = None,
    ) -> Self:
        current_hue, current_saturation, current_value = self.as_hsv_tuple

        return self.from_hsv(
            current_hue if hue is None else hue,
            current_saturation if saturation is None else saturation,
            current_value if value is None else value,
            self.alpha,
        )

    def with_hue(self, hue: int | float) -> Self:
        return self.with_hsv(hue=hue)

    def with_saturation(self, saturation: int | float) -> Self:
        return self.with_hsv(saturation=saturation)

    def with_value(self, value: int | float) -> Self:
        return self.with_hsv(value=value)

    @classmethod
    def _random_with_lightness(
            cls,
            lightness: int | float,
    ) -> Self:
        red, green, blue = colorsys.hls_to_rgb(random.random(), lightness, 1)
        return cls(red, green, blue)

    @classmethod
    def _validate_color_float(
            cls,
            value: int | float,
    ) -> int | float:
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a real number")

        if value < 0 or value > 1:
            raise ValueError("Value must be a real number between 0 and 1")

        return value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"red={self.red:.3f}, green={self.green:.3f}, blue={self.blue:.3f}, alpha={self.alpha:.3f})"
        )
