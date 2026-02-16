from dataclasses import dataclass
from typing import Any

from pyglet.graphics import Group
from pyglet.shapes import Circle as CircleBase, Rectangle as RectangleBase

from simpli.enums import LayerGroup
from simpli.utils import Vector, Color, Value
from ._shape import Shape
from ._shape_holder import AbstractShapeHolder, ShapeHolder


@dataclass(kw_only=True, slots=True)
class Circle(Shape):
    position: Vector = Vector.zero()
    radius: float = 0
    color: Color = Color.black()

    _previous_position: Vector = None
    _previous_radius: float = None
    _previous_color: Color = None
    _previous_zoom: float = None

    def __post_init__(self) -> None:
        self._previous_visible = self.visible
        self._previous_layer_group = LayerGroup(self.layer_group.value)
        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_radius = self.radius.real
        self._previous_color = Color(*self.color.as_tuple)
        self._previous_zoom = self.app.camera.zoom

        self._base = self.create()

    @property
    def is_visible(self) -> bool:
        return self.app.camera.captures_radius(self.position, self.radius)

    @property
    def segments(self) -> int:
        return int(self.radius ** 0.5 * 3.5 * self.app.camera.zoom) + 5

    def create(self) -> CircleBase:
        return CircleBase(
            self.position.x,
            self.position.y,
            self.radius,
            self.segments,
            self.color.as_int_tuple,
            batch=self.app.batch,
            group=Group(self.layer_group),
            program=self.app.program,
        )

    def update(self) -> None:
        self.visible = self.is_visible

        if (
                self.layer_group == self._previous_layer_group
                and self.radius == self._previous_radius
                and self.app.camera.zoom == self._previous_zoom
        ):
            if self.visible != self._previous_visible:
                self._base.visible = self.visible
            if self.position != self._previous_position:
                self._base.position = self.position.as_tuple
            if self.color != self._previous_color:
                self._base.color = self.color.as_int_tuple
        else:
            self.remove()
            self._base = self.create()
            self._base.visible = self.visible

        self._previous_visible = self.visible
        self._previous_layer_group = LayerGroup(self._previous_layer_group.value)
        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_radius = self.radius.real
        self._previous_color = Color(*self.color.as_tuple)
        self._previous_zoom = self.app.camera.zoom


@dataclass(kw_only=True, slots=True)
class Rectangle(Shape):
    position: Vector = Vector.zero()
    width: float = 0
    height: float = 0
    color: Color = Color.black()

    _previous_position: Vector = None
    _previous_width: float = None
    _previous_height: float = None
    _previous_color: Color = None

    def __post_init__(self) -> None:
        self._previous_visible = self.visible
        self._previous_layer_group = LayerGroup(self.layer_group.value)
        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_width = self.width.real
        self._previous_height = self.height.real
        self._previous_color = Color(*self.color.as_tuple)

        self._base = self.create()

    @property
    def is_visible(self) -> bool:
        return True

    def create(self) -> Any:
        return RectangleBase(
            self.position.x,
            self.position.y,
            self.width,
            self.height,
            self.color.as_int_tuple,
            batch=self.app.batch,
            group=Group(self.layer_group),
            program=self.app.program,
        )

    def update(self) -> None:
        self.visible = self.is_visible

        if (
                self.layer_group == self._previous_layer_group
        ):
            if self.position != self._previous_position:
                self._base.position = self.position.as_tuple
            if self.width != self._previous_width:
                self._base.width = self.width.real
            if self.height != self._previous_height:
                self._base.height = self.height.real
            if self.color != self._previous_color:
                self._base.color = self.color.as_int_tuple
        else:
            self.remove()
            self._base = self.create()
            self._base.visible = self.visible

        self._previous_visible = self.visible
        self._previous_layer_group = LayerGroup(self._previous_layer_group.value)
        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_width = self.width.real
        self._previous_height = self.height.real
        self._previous_color = Color(*self.color.as_tuple)


@dataclass(kw_only=True, slots=True)
class BackgroundRectangle(Rectangle):
    layer_group: LayerGroup = LayerGroup.BACKGROUND

    def __post_init__(self) -> None:
        self.visible = self.is_visible

        self.position = Value(lambda: self.app.camera.position_from_window(Vector.zero()))
        self.width = Value(lambda: self.app.window_width / self.app.camera.zoom)
        self.height = Value(lambda: self.app.window_height / self.app.camera.zoom)
        self.color = Value(lambda: self.app.window_background_color)

        self._previous_visible = self.visible
        self._previous_layer_group = LayerGroup(self.layer_group.value)
        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_width = float(self.width.real)
        self._previous_height = float(self.height.real)
        self._previous_color = Color(*self.color.as_tuple)

        self._base = self.create()

    @property
    def is_visible(self) -> bool:
        return True

    def create(self) -> Any:
        return RectangleBase(
            self.position.x,
            self.position.y,
            self.width,
            self.height,
            self.color.as_int_tuple,
            batch=self.app.batch,
            group=Group(self.layer_group),
            program=self.app.grid_program,
        )


__all__ = [
    Shape,
    AbstractShapeHolder,
    ShapeHolder,
    Circle,
    Rectangle,
    BackgroundRectangle,
]
