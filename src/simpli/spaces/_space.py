from abc import ABC, abstractmethod

from simpli.resources import ResourceHolder


class Space(ABC):
    @property
    @abstractmethod
    def resources(self) -> ResourceHolder:
        ...

    @abstractmethod
    def step(
            self,
            delta: int | float,
    ) -> None:
        ...
