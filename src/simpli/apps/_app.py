from abc import ABC, abstractmethod

from pyglet.window import Window

from simpli.counters import Counter
from simpli.renderers import Renderer
from simpli.spaces import Space


class App(ABC):
    @property
    @abstractmethod
    def title(self) -> str:
        ...

    @property
    @abstractmethod
    def space(self) -> Space:
        ...

    @property
    @abstractmethod
    def renderer(self) -> Renderer:
        ...

    @property
    @abstractmethod
    def counter(self) -> Counter:
        ...

    @property
    @abstractmethod
    def window(self) -> Window:
        ...

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...
