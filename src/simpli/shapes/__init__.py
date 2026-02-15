from dataclasses import dataclass
from math import sqrt
from typing import TypeVar, Callable, TypeAlias

from pyglet.graphics import Group
from pyglet.shapes import Circle as CircleBase

from simpli.utils import Vector, Color
from ._shape import Shape
from ._shape_holder import AbstractShapeHolder, ShapeHolder

_T = TypeVar('_T', bound=object)
_EntityAttributeGetter: TypeAlias = Callable[[], _T]


@dataclass(kw_only=True, slots=True)
class Circle(Shape):
    position_getter: _EntityAttributeGetter[Vector]
    radius_getter: _EntityAttributeGetter[float]
    color_getter: _EntityAttributeGetter[Color]

    position: Vector = Vector.zero()
    radius: float = 0
    color: Color = Color.black()

    _circle: CircleBase = None
    _previous_radius: float = 0

    def __post_init__(self) -> None:
        self._circle: CircleBase = self.create()

    @property
    def segments(self) -> int:
        return int(sqrt(self.radius) * 7.5) + 5

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
        self._update_values()

        if self.radius == self._previous_radius:
            self._circle.x = self.position.x
            self._circle.y = self.position.y
            self._circle.color = self.color.as_int_tuple
        else:
            self.remove()
            self._circle = self.create()
            self._previous_radius = self.radius

    def _update_values(self) -> None:
        self.layer_group = self.layer_group_getter()
        self.position = self.position_getter()
        self.radius = self.radius_getter()
        self.color = self.color_getter()

    def remove(self) -> None:
        self._circle.delete()


__all__ = [
    Shape,
    AbstractShapeHolder,
    ShapeHolder,
    Circle,
]
