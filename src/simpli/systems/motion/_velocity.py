from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.spaces import Space
from simpli.systems import TickSystem
from simpli.utils import Supplier


class VelocitySystem(TickSystem):
    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for entity in space.entities.by_components(PositionComponent, VelocityComponent):
            position: PositionComponent = entity.get(PositionComponent)

            if isinstance(position.position, Supplier):
                continue

            position.position += entity.get(VelocityComponent).velocity * delta
