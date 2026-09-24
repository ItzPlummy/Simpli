from abc import ABC, abstractmethod

from simpli.entities import EntityHolder
from simpli.resources import ResourceHolder
from simpli.systems import SystemHolder


class Space(ABC):
    @property
    @abstractmethod
    def entities(self) -> EntityHolder:
        ...

    @property
    @abstractmethod
    def systems(self) -> SystemHolder:
        ...

    @property
    @abstractmethod
    def resources(self) -> ResourceHolder:
        ...

    @abstractmethod
    def on_tick(
            self,
            delta: int | float,
    ) -> None:
        ...

    @abstractmethod
    def on_frame(
            self,
            alpha: int | float,
    ) -> None:
        ...
