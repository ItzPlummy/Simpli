from dataclasses import dataclass
from typing import TypeVar, Callable, TypeAlias, Any

from pyglet.graphics import Group
from pyglet.shapes import Circle as CircleBase, Rectangle as RectangleBase

from simpli.enums import LayerGroup
from simpli.utils import Vector, Color, Value
from ._shape import Shape
from ._shape_holder import AbstractShapeHolder, ShapeHolder

_T = TypeVar('_T', bound=object)
_EntityAttributeGetter: TypeAlias = Callable[[], _T]


@dataclass(kw_only=True, slots=True)
class Circle(Shape):
    position: Vector = Vector.zero()
    radius: float = 0
    color: Color = Color.black()

    _previous_position: Vector = None
    _previous_radius: float = None
    _previous_color: Color = None
    _previous_zoom: float = None

    _circle: CircleBase = None

    def __post_init__(self) -> None:
        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_radius = float(self.radius.real)
        self._previous_color = Color(*self.color.as_tuple)
        self._previous_zoom: float = self.app.camera.zoom

        self._circle: CircleBase = self.create()

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
        # print(self.position, self._previous_position)

        if self.radius == self._previous_radius and self.app.camera.zoom == self._previous_zoom:
            if self.position != self._previous_position:
                self._circle.position = self.position.as_tuple
            if self.color != self._previous_color:
                self._circle.color = self.color.as_int_tuple
        else:
            self.remove()
            self._circle = self.create()

        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_radius = float(self.radius.real)
        self._previous_color = Color(*self.color.as_tuple)
        self._previous_zoom = self.app.camera.zoom

    def remove(self) -> None:
        self._circle.delete()


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

    _rectangle: RectangleBase = None

    def __post_init__(self) -> None:
        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_width = float(self.width.real)
        self._previous_height = float(self.height.real)
        self._previous_color = Color(*self.color.as_tuple)

        self._rectangle: RectangleBase = self.create()

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
        if self.position != self._previous_position:
            self._rectangle.position = self.position.as_tuple
            self._previous_position = Vector(*self.position.as_tuple)
        if self.width != self._previous_width:
            self._rectangle.width = float(self.width.real)
            self._previous_width = float(self.width.real)
        if self.height != self._previous_height:
            self._rectangle.height = float(self.height.real)
            self._previous_height = float(self.height.real)
        if self.color != self._previous_color:
            self._rectangle.color = self.color.as_int_tuple
            self._previous_color = Color(*self.color.as_tuple)

    def remove(self) -> None:
        self._rectangle.delete()


@dataclass(kw_only=True, slots=True)
class BackgroundRectangle(Rectangle):
    layer_group: LayerGroup = LayerGroup.BACKGROUND

    def __post_init__(self) -> None:
        self.position = Value(lambda: self.app.camera.position_from_window(Vector.zero()))
        self.width = Value(lambda: self.app.window_width / self.app.camera.zoom)
        self.height = Value(lambda: self.app.window_height / self.app.camera.zoom)
        self.color = Value(lambda: self.app.window_background_color)

        self._previous_position = Vector(*self.position.as_tuple)
        self._previous_width = float(self.width.real)
        self._previous_height = float(self.height.real)
        self._previous_color = Color(*self.color.as_tuple)

        self._rectangle: RectangleBase = self.create()

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
