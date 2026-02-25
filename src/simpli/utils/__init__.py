from ._archetype_holder import AbstractArchetypeHolder, ArchetypeHolder
from ._color import Color
from ._holder import AbstractHolder, Holder
from ._identifiable_holder import AbstractIdentifiableHolder, IdentifiableHolder
from ._value import Value
from ._vector import Vector


def safe_power(value: float, power: float) -> float:
    module_value: float = abs(value)
    return module_value ** power * (value // module_value)


__all__ = [
    AbstractArchetypeHolder,
    ArchetypeHolder,
    Color,
    AbstractHolder,
    Holder,
    AbstractIdentifiableHolder,
    IdentifiableHolder,
    Value,
    Vector,
]
