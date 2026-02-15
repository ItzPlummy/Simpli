from simpli.components import VelocityComponent, PositionComponent, AirFrictionComponent, RepulsionComponent
from simpli.utils import Vector, safe_power
from ._system import System, TickSystem
from ._system_holder import AbstractSystemHolder, SystemHolder


class ShapeUpdateSystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "shape_update"

    def tick(self) -> None:
        for shape in self.app.shapes:
            shape.update()


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

            velocity *= 1 - air_friction
            if velocity.length_squared < 0.01:
                velocity = Vector.zero()

            entity.components.get(VelocityComponent).velocity = velocity


class RepulsionSystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "repulsion"

    def tick(self) -> None:
        for entity in self.app.entities.by_components(PositionComponent, VelocityComponent, RepulsionComponent):
            position: Vector = entity.components.get(PositionComponent).position
            repulsion_velocity: Vector = Vector.zero()

            for another_entity in self.app.entities.by_components(PositionComponent, RepulsionComponent):
                if entity.identifier == another_entity.identifier:
                    continue

                distance: Vector = position - another_entity.components.get(PositionComponent).position

                if distance.length_squared < 0.01:
                    distance = Vector.random() * 0.0001

                repulsion_strength: float = another_entity.components.get(RepulsionComponent).repulsion_strength
                repulsion_range: float = another_entity.components.get(RepulsionComponent).repulsion_range
                repulsion_power_factor: float = another_entity.components.get(RepulsionComponent).repulsion_power_factor

                distance_ratio: float = distance.length / repulsion_range

                if distance_ratio > 1:
                    continue

                repulsion_velocity += (
                        distance.normalized
                        * (1 - safe_power(distance_ratio, repulsion_power_factor))
                        * repulsion_strength
                )

            entity.components.get(VelocityComponent).velocity += repulsion_velocity


__all__ = [
    System,
    TickSystem,
    AbstractSystemHolder,
    SystemHolder,
]
