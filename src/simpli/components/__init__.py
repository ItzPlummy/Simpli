from dataclasses import dataclass

from simpli.shapes import Shape
from simpli.utils import Vector, Color
from ._component import Component
from ._component_holder import AbstractComponentHolder, ComponentHolder


@dataclass(kw_only=True, slots=True)
class PositionComponent(Component):
    position: Vector = Vector.zero()

    @classmethod
    def tag(cls) -> str:
        return "position"


@dataclass(kw_only=True, slots=True)
class VelocityComponent(Component):
    velocity: Vector = Vector.zero()

    @classmethod
    def tag(cls) -> str:
        return "velocity"


@dataclass(kw_only=True, slots=True)
class AirFrictionComponent(Component):
    air_friction: float = 0.035

    @classmethod
    def tag(cls) -> str:
        return "air_friction"


@dataclass
class RepulsionComponent(Component):
    repulsion_strength: float = 1
    repulsion_range: float = 50
    repulsion_power_factor: float = 1

    @classmethod
    def tag(cls) -> str:
        return "repulsion"


@dataclass(kw_only=True, slots=True)
class ShapeComponent(Component):
    shape: Shape

    @classmethod
    def tag(cls) -> str:
        return "shape"


@dataclass(kw_only=True, slots=True)
class CircleComponent(Component):
    radius: float = 50
    color: Color = Color.black()

    @classmethod
    def tag(cls) -> str:
        return "circle"


__all__ = [
    Component,
    ComponentHolder,
    PositionComponent,
    VelocityComponent,
    AirFrictionComponent,
    RepulsionComponent,
    ShapeComponent,
]
