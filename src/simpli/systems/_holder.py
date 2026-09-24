from abc import ABC, abstractmethod
from typing import Iterable

from simpli.systems._system import System


class SystemHolder(ABC):
    @abstractmethod
    def add(
            self,
            system: System,
    ) -> None:
        ...

    @abstractmethod
    def get[T: System](
            self,
            system: type[T],
    ) -> T:
        ...

    @abstractmethod
    def find[T: System](
            self,
            system: type[T],
    ) -> T | None:
        ...

    @abstractmethod
    def has(
            self,
            system: type[System],
    ) -> bool:
        ...

    @abstractmethod
    def remove(
            self,
            system: type[System],
    ) -> None:
        ...

    @abstractmethod
    def of_kind[T: System](
            self,
            system: type[T],
    ) -> Iterable[T]:
        ...
