from typing import Type, Any

from simpli.shapes import Shape
from simpli.utils import Vector
from ._component import Component
from ._component_holder import AbstractComponentHolder, ComponentHolder


class ShapeComponent(Component):
    def __component_init__(self, shape: Type[Shape], **kwargs: Any) -> None:
        self.shape = shape(app=self.app, entity=self.entity, **kwargs)

    @classmethod
    def tag(cls) -> str:
        return "shape"


class PositionComponent(Component):
    def __component_init__(self, position: Vector | None = None) -> None:
        self.position = position or Vector.zero()

    @classmethod
    def tag(cls) -> str:
        return "position"


class VelocityComponent(Component):
    def __component_init__(self, velocity: Vector | None = None) -> None:
        self.velocity = velocity or Vector.zero()

    @classmethod
    def tag(cls) -> str:
        return "velocity"


class AirFrictionComponent(Component):
    def __component_init__(self, air_friction: float | None = None) -> None:
        self.air_friction = air_friction or 0.975

    @classmethod
    def tag(cls) -> str:
        return "air_friction"


class GravityComponent(Component):
    def __component_init__(self, gravity: Vector | None = None) -> None:
        self.gravity = gravity or Vector(0, -0.25)

    @classmethod
    def tag(cls) -> str:
        return "gravity"


__all__ = [
    Component,
    ComponentHolder,
    ShapeComponent,
    PositionComponent,
    VelocityComponent,
    AirFrictionComponent,
    GravityComponent,
]
