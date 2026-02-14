from simpli.components import VelocityComponent, PositionComponent, AirFrictionComponent, ShapeComponent, \
    GravityComponent
from simpli.utils import Vector
from ._system import System, TickSystem
from ._system_holder import AbstractSystemHolder, SystemHolder


class ShapeRenderSystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "shape_render"

    def tick(self) -> None:
        for entity in self.app.entities.by_components(ShapeComponent):
            entity.components.get(ShapeComponent).shape.update()


class VelocitySystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "velocity"

    def tick(self) -> None:
        for entity in self.app.entities.by_components(PositionComponent, VelocityComponent):
            velocity: Vector = entity.components.get(VelocityComponent).velocity
            entity.components.get(PositionComponent).position += velocity


class AirFrictionSystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "air_friction"

    def tick(self) -> None:
        for entity in self.app.entities.by_components(VelocityComponent, AirFrictionComponent):
            velocity: Vector = entity.components.get(VelocityComponent).velocity
            air_friction: float = entity.components.get(AirFrictionComponent).air_friction

            velocity *= air_friction
            if velocity.length_squared < 0.01:
                velocity = Vector.zero()

            entity.components.get(VelocityComponent).velocity = velocity


class GravitySystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "gravity"

    def tick(self) -> None:
        for entity in self.app.entities.by_components(VelocityComponent, GravityComponent):
            entity.components.get(VelocityComponent).velocity += entity.components.get(GravityComponent).gravity


__all__ = [
    System,
    TickSystem,
    AbstractSystemHolder,
    SystemHolder,
]
