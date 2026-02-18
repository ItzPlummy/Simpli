from typing import TypeVar, Generic, FrozenSet, Self

from simpli.interfaces import Tagged

_T = TypeVar("_T", bound=Tagged)


class Signature(Generic[_T]):
    def __init__(
            self,
            *values: _T,
    ) -> None:
        self._values: FrozenSet[str] = frozenset(map(lambda value: value.tag(), values))

    def __eq__(self, other: Self) -> bool:
        return self._values == other._values
