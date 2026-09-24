from collections import defaultdict
from typing import Iterable

from simpli.systems._system import System
from simpli.systems._holder import SystemHolder


class DefaultSystemHolder(SystemHolder):
    def __init__(self) -> None:
        self._systems: dict[str, dict[str, System]] = defaultdict[str, dict[str, System]](dict)

    def add(
            self,
            system: System,
    ) -> None:
        self._systems[system.kind()][system.tag()] = system

    def get[T: System](
            self,
            system: type[T],
    ) -> T | None:
        if system.kind() not in self._systems:
            return None

        return self._systems[system.kind()].get(system.tag())

    def has(
            self,
            system: type[System],
    ) -> bool:
        if system.kind() not in self._systems:
            return False

        return system.tag() in self._systems[system.kind()]

    def remove(
            self,
            system: type[System],
    ) -> None:
        if system.kind() in self._systems:
            self._systems[system.kind()].pop(system.tag(), None)

    def of_kind[T: System](
            self,
            system: type[T],
    ) -> Iterable[T]:
        if system.kind() not in self._systems:
            return []

        return self._systems[system.kind()].values()
