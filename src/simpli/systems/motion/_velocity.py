from simpli.components.motion import Position, Velocity
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
        for entity in space.entities.by_components(Position, Velocity):
            entity.get(Position).position += entity.get(Velocity).velocity * delta
