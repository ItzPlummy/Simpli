from typing import Never, Any

from pyglet.app import run
from pyglet.gl import Config, glClearColor
from pyglet.graphics import Batch
from pyglet.graphics.shader import ShaderProgram, Shader
from pyglet.window import Window

from simpli.components import PositionComponent, VelocityComponent, AirFrictionComponent, ShapeComponent
from simpli.entities import AbstractEntityHolder, EntityHolder, Entity, AbstractEntity
from simpli.internal import Shaders
from simpli.shapes import Circle
from simpli.systems import AbstractSystemHolder, SystemHolder, TickSystem, VelocitySystem, AirFrictionSystem, \
    ShapeRenderSystem, GravitySystem
from simpli.utils import Color, Vector


class Simpli:
    def __init__(
            self,
            title: str = "Simpli",
            *,
            window_width: int = 1280,
            window_height: int = 720,
            window_background_color: Color = Color(0.95, 0.95, 0.95),
            **window_kwargs: Any
    ) -> None:
        self._title: str = title
        self._window_width: int = window_width
        self._window_height: int = window_height
        self._window_background_color: Color = window_background_color

        self._window = Window(
            caption=self._title,
            width=self._window_width,
            height=self._window_height,
            config=Config(sample_buffers=1, samples=4),
            **window_kwargs
        )

        glClearColor(*self._window_background_color.as_tuple)

        self._batch = Batch()

        self._program = ShaderProgram(
            Shader(Shaders.VERTEX_SHADER, "vertex"),
            Shader(Shaders.FRAGMENT_SHADER, "fragment"),
        )
        self._layout_program = ShaderProgram(
            Shader(Shaders.LAYOUT_VERTEX_SHADER, "vertex"),
            Shader(Shaders.LAYOUT_FRAGMENT_SHADER, "fragment"),
        )

        self._system_holder: AbstractSystemHolder = SystemHolder(self)
        self._entities: AbstractEntityHolder = EntityHolder(self)

        self._system_holder.add(
            VelocitySystem,
            AirFrictionSystem,
            GravitySystem,
            ShapeRenderSystem,
        )

        self._window.set_handler("on_draw", self._tick)

    @property
    def title(self) -> str:
        return self._title

    @property
    def window_width(self) -> int:
        return self._window_width

    @property
    def window_height(self) -> int:
        return self._window_height

    @property
    def window_background_color(self) -> Color:
        return self._window_background_color

    @property
    def window(self) -> Window:
        return self._window

    @property
    def batch(self) -> Batch:
        return self._batch

    @property
    def program(self) -> ShaderProgram:
        return self._program

    @property
    def layout_program(self) -> ShaderProgram:
        return self._layout_program

    @property
    def system_holder(self) -> AbstractSystemHolder:
        return self._system_holder

    @property
    def entities(self) -> AbstractEntityHolder:
        return self._entities

    def run(self) -> Never:
        run()  # More logic upcoming, method won't be static

    def _tick(self) -> None:
        self._window.clear()

        for system in self._system_holder.by_system(TickSystem):
            system.tick()

        self._program["u_window_size"] = self._window.size
        self._program["u_camera_position"] = (0, 0)
        self._program["u_zoom"] = 1

        self._layout_program["u_window_size"] = (*self._window.size, 0)
        self._layout_program["u_camera_position"] = (0, 0, 0)
        self._layout_program["u_zoom"] = 1

        self._batch.draw()


__all__ = [
    Simpli
]
