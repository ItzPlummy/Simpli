from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.spaces import Space
from simpli.systems import TickSystem


class VelocitySystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "velocity"

    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for entity in space.entities.by_components(PositionComponent, VelocityComponent):
            entity.get(PositionComponent).position += entity.get(VelocityComponent).velocity * delta
