from simpli.components.motion import VelocityComponent
from simpli.spaces import Space
from simpli.systems import TickSystem
from simpli.utils import Resolvable, resolve, Vector


class AirResistanceSystem(TickSystem):
    _DEFAULT_RESISTANCE: int | float = 0.5

    def __init__(
            self,
            *,
            resistance: Resolvable[int | float] | None = None,
    ) -> None:
        self._resistance: Resolvable[int | float] = resistance if resistance is not None else self._DEFAULT_RESISTANCE

    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for entity in space.entities.by_components(VelocityComponent):
            velocity: VelocityComponent = entity.get(VelocityComponent)

            resistance: int | float = resolve(self._resistance) * delta

            if resistance <= 0:
                return

            if resistance >= 1:
                velocity.velocity = Vector.zero()

            velocity.velocity *= (1 - resistance)
