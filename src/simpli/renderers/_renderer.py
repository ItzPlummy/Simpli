from abc import ABC, abstractmethod

from pyglet.graphics import Group, Batch
from pyglet.window import Window

from simpli.resources import Resource


class Renderer(Resource, ABC):
    @classmethod
    def tag(cls) -> str:
        return "renderer"

    @property
    @abstractmethod
    def batch(self) -> Batch:
        ...

    @abstractmethod
    def draw(
            self,
            window: Window,
    ) -> None:
        ...

    @abstractmethod
    def layer(
            self,
            order: int,
    ) -> Group:
        ...
