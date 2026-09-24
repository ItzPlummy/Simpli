from abc import ABC, abstractmethod

from simpli.counters._time import Time
from simpli.utils import Resolvable


class Counter(ABC):
    @property
    @abstractmethod
    def tps(self) -> int | float:
        ...

    @tps.setter
    @abstractmethod
    def tps(self, tps: Resolvable[int | float]):
        ...

    @property
    @abstractmethod
    def fps(self) -> int | float:
        ...

    @fps.setter
    @abstractmethod
    def fps(self, fps: Resolvable[int | float]):
        ...

    @property
    @abstractmethod
    def time_scale(self) -> Resolvable[int | float]:
        ...

    @time_scale.setter
    @abstractmethod
    def time_scale(self, time_scale: Resolvable[int | float]) -> None:
        ...

    @property
    @abstractmethod
    def is_paused(self) -> bool:
        ...

    @is_paused.setter
    @abstractmethod
    def is_paused(self, is_paused: Resolvable[bool]) -> None:
        ...

    @property
    @abstractmethod
    def time(self) -> Time:
        ...

    @abstractmethod
    def advance(
            self,
            real_delta: int | float,
    ) -> int | float:
        ...

    @abstractmethod
    def step(self) -> None:
        ...
