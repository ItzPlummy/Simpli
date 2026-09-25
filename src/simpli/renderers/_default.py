from pyglet.gl import glClearColor
from pyglet.graphics import Batch, Group
from pyglet.window import Window

from simpli.renderers._renderer import Renderer
from simpli.utils import Color


class DefaultRenderer(Renderer):
    def __init__(
            self,
            clear_color: Color,
    ) -> None:
        self._clear_color = clear_color

        self._batch = Batch()
        self._layers: dict[int, Group] = {}

    @property
    def batch(self) -> Batch:
        return self._batch

    def draw(
            self,
            window: Window,
    ) -> None:
        glClearColor(*self._clear_color.as_tuple)
        window.clear()
        self._batch.draw()

    def layer(
            self,
            order: int,
    ) -> Group:
        group = self._layers.get(order)

        if group is None:
            group = self._layers[order] = Group(order=order)

        return group
