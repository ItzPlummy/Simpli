from collections import defaultdict
from typing import Iterable

from simpli.systems._system import System
from simpli.systems._holder import SystemHolder


class DefaultSystemHolder(SystemHolder):
    def __init__(self) -> None:
        self._systems: dict[type[System], System] = {}
        self._kinds: dict[type[System], dict[type[System], System]] = defaultdict[type[System], dict[type[System], System]](dict)

    def add(
            self,
            system: System,
    ) -> None:
        self._systems[type(system)] = system

        for kind in System.get_kinds():
            if isinstance(system, kind):
                self._kinds[kind][type(system)] = system

    def get[T: System](
            self,
            system: type[T],
    ) -> T:
        try:
            return self._systems[system]
        except KeyError:
            raise RuntimeError(f"Unable to get system")

    def find[T: System](
            self,
            system: type[T],
    ) -> T | None:
        try:
            return self._systems[system]
        except KeyError:
            return None

    def has(
            self,
            system: type[System],
    ) -> bool:
        return system in self._systems

    def remove(
            self,
            system: type[System],
    ) -> None:
        self._systems.pop(system, None)

        for kind in System.get_kinds():
            if issubclass(system, kind):
                self._kinds[kind].pop(system, None)

    def of_kind[T: System](
            self,
            system: type[T],
    ) -> Iterable[T]:
        return self._kinds[system].values()
