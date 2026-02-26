from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Self, FrozenSet

from ._tagged import Tagged

_T = TypeVar("_T", bound=Tagged)


class Archetype(Generic[_T]):
    __slots__ = ("_values",)

    def __init__(
            self,
            *values: _T,
    ) -> None:
        self._values: FrozenSet[str] = frozenset(map(lambda value: value.tag(), values))

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Archetype):
            return False
        return self._values == other._values

    def __ge__(self, other: Self) -> bool:
        if not isinstance(other, Archetype):
            return False
        return self._values >= other._values

    def __le__(self, other: Self) -> bool:
        if not isinstance(other, Archetype):
            return False
        return self._values <= other._values

    def __hash__(self) -> int:
        return hash(self._values)


class Archetyped(Generic[_T], ABC):
    @property
    @abstractmethod
    def archetype(self) -> Archetype[_T]:
        raise NotImplementedError
