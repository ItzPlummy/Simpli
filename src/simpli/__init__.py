from typing import Never, Any

import pyglet
from pyglet.app import run
from pyglet.gl import Config, glClearColor
from pyglet.graphics import Batch
from pyglet.graphics.shader import ShaderProgram, Shader
from pyglet.window import Window

from simpli.camera import AbstractCamera, Camera
from simpli.components import PositionComponent, VelocityComponent, AirFrictionComponent, ShapeComponent
from simpli.entities import AbstractEntityHolder, EntityHolder, Entity, AbstractEntity, BackgroundEntity
from simpli.enums import MouseButton, LayerGroup
from simpli.internal import Shaders
from simpli.shapes import Circle
from simpli.shapes import ShapeHolder, AbstractShapeHolder
from simpli.systems import AbstractSystemHolder, SystemHolder, TickSystem, VelocitySystem, AirFrictionSystem, \
    ShapeUpdateSystem, RepulsionSystem, AttractionSystem
from simpli.utils import Color, Vector


class Simpli:
    def __init__(
            self,
            title: str = "Simpli",
            *,
            window_width: int = 1280,
            window_height: int = 720,
            window_background_color: Color = Color(0.95, 0.95, 0.95),
            tps: float = 60.0,
            **window_kwargs: Any
    ) -> None:
        self._title: str = title
        self._window_width: int = window_width
        self._window_height: int = window_height
        self._window_background_color: Color = window_background_color
        self._tps: float = tps

        self._window = Window(
            caption=self._title,
            width=self._window_width,
            height=self._window_height,
            config=Config(sample_buffers=1, samples=4),
            **window_kwargs
        )

        glClearColor(*self._window_background_color.as_tuple)

        self._batch = Batch()
        self._groups = {layer_group: layer_group.value for layer_group in LayerGroup}

        self._program = ShaderProgram(
            Shader(Shaders.VERTEX_SHADER, "vertex"),
            Shader(Shaders.FRAGMENT_SHADER, "fragment"),
        )
        self._layout_program = ShaderProgram(
            Shader(Shaders.LAYOUT_VERTEX_SHADER, "vertex"),
            Shader(Shaders.LAYOUT_FRAGMENT_SHADER, "fragment"),
        )
        self._grid_program = ShaderProgram(
            Shader(Shaders.GRID_VERTEX_SHADER, "vertex"),
            Shader(Shaders.GRID_FRAGMENT_SHADER, "fragment"),
        )

        self._camera: AbstractCamera = Camera(app=self)
        self._systems: AbstractSystemHolder = SystemHolder(app=self)
        self._entities: AbstractEntityHolder = EntityHolder(app=self)
        self._shapes: AbstractShapeHolder = ShapeHolder(app=self)

        self._systems.add(
            VelocitySystem,
            AirFrictionSystem,
            AttractionSystem,
            RepulsionSystem,
            ShapeUpdateSystem,
        )

        self._window_mouse_position: Vector = Vector.zero()

        self._entities.new(BackgroundEntity)

        self._window.set_handler("on_draw", self._tick)
        self._window.set_handler("on_mouse_motion", self._mouse_move)
        self._window.set_handler("on_mouse_press", self._mouse_click)
        self._window.set_handler("on_mouse_scroll", self._mouse_scroll)

        self.on_startup()
        self.a = pyglet.window.FPSDisplay(self._window)

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
    def tps(self) -> float:
        return self._tps

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
    def grid_program(self) -> ShaderProgram:
        return self._grid_program

    @property
    def camera(self) -> AbstractCamera:
        return self._camera

    @property
    def systems(self) -> AbstractSystemHolder:
        return self._systems

    @property
    def entities(self) -> AbstractEntityHolder:
        return self._entities

    @property
    def shapes(self) -> AbstractShapeHolder:
        return self._shapes

    @property
    def mouse_position(self) -> Vector:
        return self._camera.target_position_from_window(self.window_mouse_position)

    @property
    def window_mouse_position(self) -> Vector:
        return self._window_mouse_position

    def run(self) -> Never:
        run(interval=1 / self._tps)

    def on_startup(self) -> None:
        pass

    def on_tick(self) -> None:
        pass

    def on_mouse_move(
            self,
            position: Vector,
            distance: Vector,
    ) -> None:
        pass

    def on_mouse_click(
            self,
            position: Vector,
            button: MouseButton,
    ) -> None:
        pass

    def on_mouse_scroll(
            self,
            position: Vector,
            scroll: float,
    ) -> None:
        pass

    def _tick(self) -> None:
        self.on_tick()
        self._camera.tick()
        self._window.clear()

        for system in self._systems.by_system(TickSystem):
            system.tick()

        self._program["u_window_size"] = self._window.size
        self._program["u_camera_position"] = self._camera.position.as_tuple
        self._program["u_zoom"] = self._camera.zoom

        self._layout_program["u_window_size"] = (*self._window.size, 0)
        self._layout_program["u_camera_position"] = (*self._camera.position.as_tuple, 0)
        self._layout_program["u_zoom"] = self._camera.zoom

        self._grid_program["u_window_size"] = self._window.size
        self._grid_program["u_camera_position"] = self._camera.position.as_tuple
        self._grid_program["u_zoom"] = self._camera.zoom

        self._batch.draw()
        self.a.draw()

    def _mouse_move(
            self,
            x: int,
            y: int,
            dx: int,
            dy: int,
    ) -> None:
        self._window_mouse_position = Vector(x, y)
        self.on_mouse_move(self.mouse_position, self._camera.position_from_window(Vector(dx, dy)))

    def _mouse_click(
            self,
            x: int,
            y: int,
            button: int,
            modifiers: int,
    ) -> None:
        try:
            button: MouseButton = MouseButton(button)
        except ValueError:
            return

        self.on_mouse_click(self._camera.position_from_window(Vector(x, y)), button)

    def _mouse_scroll(
            self,
            x: int,
            y: int,
            scroll_x: float,
            scroll_y: float,
    ) -> None:
        scroll: float = scroll_y if abs(scroll_y) >= abs(scroll_x) else scroll_x

        self._camera.adjust_zoom_by_scroll(scroll)
        self.on_mouse_scroll(self._camera.position_from_window(Vector(x, y)), scroll)


__all__ = [
    Simpli
]
