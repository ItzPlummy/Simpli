from simpli.components import VelocityComponent, PositionComponent, AirFrictionComponent, RepulsionComponent, \
    AttractionComponent
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
            velocity: Vector = entity.get_component(VelocityComponent).velocity
            entity.get_component(PositionComponent).position += velocity


class AirFrictionSystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "air_friction"

    def tick(self) -> None:
        for entity in self.app.entities.by_components(VelocityComponent, AirFrictionComponent):
            velocity: Vector = entity.get_component(VelocityComponent).velocity
            air_friction: float = entity.get_component(AirFrictionComponent).air_friction

            velocity *= 1 - air_friction
            if velocity.length_squared < 0.01:
                velocity = Vector.zero()

            entity.get_component(VelocityComponent).velocity = velocity


class AttractionSystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "attraction"

    def tick(self) -> None:
        for entity in self.app.entities.by_components(PositionComponent, AttractionComponent):
            position: Vector = entity.get_component(PositionComponent).position
            attraction: AttractionComponent = entity.get_component(AttractionComponent)

            for nearby_entity in self.app.entities.nearby(
                    position,
                    attraction.range,
                    PositionComponent,
                    VelocityComponent,
            ):
                if entity.identifier == nearby_entity.identifier:
                    continue

                distance: Vector = position - nearby_entity.get_component(PositionComponent).position

                if distance.length_squared < 0.001:
                    distance = Vector.random() * 0.1

                distance_ratio: float = distance.length / attraction.range

                nearby_entity.get_component(VelocityComponent).velocity += (
                        distance.normalized
                        * (1 - safe_power(distance_ratio, attraction.power_factor))
                        * attraction.strength
                )


class RepulsionSystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "repulsion"

    def tick(self) -> None:
        for entity in self.app.entities.by_components(PositionComponent, RepulsionComponent):
            position: Vector = entity.get_component(PositionComponent).position
            repulsion: RepulsionComponent = entity.get_component(RepulsionComponent)

            for nearby_entity in self.app.entities.nearby(
                    position,
                    repulsion.range,
                    PositionComponent,
                    VelocityComponent,
            ):
                if entity.identifier == nearby_entity.identifier:
                    continue

                distance: Vector = nearby_entity.get_component(PositionComponent).position - position

                if distance.length_squared < 0.001:
                    distance = Vector.random() * 0.1

                distance_ratio: float = distance.length / repulsion.range

                nearby_entity.get_component(VelocityComponent).velocity += (
                        distance.normalized
                        * (1 - safe_power(distance_ratio, repulsion.power_factor))
                        * repulsion.strength
                )


__all__ = [
    System,
    TickSystem,
    AbstractSystemHolder,
    SystemHolder,
]
