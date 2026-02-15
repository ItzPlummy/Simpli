from math import sqrt
from typing import TypeVar, Any, TYPE_CHECKING, Callable, TypeAlias

from pyglet.shapes import Circle as CircleBase

from simpli.utils import Vector, Color
from ._base import Shape

if TYPE_CHECKING:
    from simpli import Simpli
    from simpli.entities import AbstractEntity
else:
    Simpli = Any
    AbstractEntity = Any


_T = TypeVar('_T', bound=object)
_EntityAttributeGetter: TypeAlias = Callable[[AbstractEntity], _T]


class Circle(Shape):
    def __init__(
            self,
            *,
            app: Simpli,
            entity: AbstractEntity,
            position_getter: _EntityAttributeGetter[Vector],
            radius_getter: _EntityAttributeGetter[float],
            color_getter: _EntityAttributeGetter[Color],
    ) -> None:
        super().__init__(app=app, entity=entity)

        self._position_getter = position_getter
        self._radius_getter = radius_getter
        self._color_getter = color_getter

        self._position: Vector
        self._radius: float
        self._color: Color

        self._update_values()
        self._circle: CircleBase = self.create()
        self._previous_radius: float = self._radius

    @property
    def position(self) -> Vector:
        return self._position

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def segments(self) -> int:
        return int(sqrt(self._radius) * 7.5) + 5

    @property
    def color(self) -> Color:
        return self._color

    def create(self) -> CircleBase:
        return CircleBase(
            self._position.x,
            self._position.y,
            self._radius,
            self.segments,
            self._color.as_int_tuple,
            batch=self.app.batch,
            program=self.app.program,
        )

    def update(self) -> None:
        self._update_values()

        if self._radius == self._previous_radius:
            self._circle.x = self._position.x
            self._circle.y = self._position.y
            self._circle.color = self._color.as_int_tuple
        else:
            self.remove()
            self._circle = self.create()

        self._previous_radius = self._radius

    def _update_values(self) -> None:
        self._position = self._position_getter(self.entity)
        self._radius = self._radius_getter(self.entity)
        self._color = self._color_getter(self.entity)

    def remove(self) -> None:
        self._circle.delete()


__all__ = [
    Shape,
    Circle,
]
