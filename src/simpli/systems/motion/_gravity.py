from simpli.components.motion import VelocityComponent
from simpli.spaces import Space
from simpli.systems import TickSystem
from simpli.utils import Resolvable, Vector, resolve


class GravitySystem(TickSystem):
    _DEFAULT_ACCELERATION: Vector = Vector(0, -25)

    def __init__(
            self,
            *,
            acceleration: Resolvable[Vector] | None = None,
    ) -> None:
        self._acceleration: Resolvable[Vector] = acceleration if acceleration is not None else self._DEFAULT_ACCELERATION

    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for entity in space.entities.by_component(VelocityComponent):
            entity.get(VelocityComponent).velocity += resolve(self._acceleration)
