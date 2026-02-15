from ._color import Color
from ._holder import AbstractHolder, Holder
from ._identifier_holder import AbstractIdentifierHolder, IdentifierHolder
from ._value import Value
from ._vector import Vector


def safe_power(value: float, power: float) -> float:
    module_value: float = abs(value)
    return module_value ** power * (value // module_value)


__all__ = [
    Color,
    AbstractHolder,
    Holder,
    AbstractIdentifierHolder,
    IdentifierHolder,
    Value,
    Vector,
]
