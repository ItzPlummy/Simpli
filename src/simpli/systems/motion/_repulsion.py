from simpli.components.motion import RepulsionComponent, VelocityComponent, PositionComponent
from simpli.spaces import Space
from simpli.systems import TickSystem
from simpli.utils import Vector, resolve, Binding, Resolvable


class RepulsionSystem(TickSystem):
    _DEFAULT_REPULSION_EXPONENT: int | float = 3

    def __init__(
            self,
            *,
            repulsion_exponent: Resolvable[int | float] | None = None,
    ) -> None:
        self._repulsion_exponent: Resolvable[int | float] = repulsion_exponent if repulsion_exponent is not None else self._DEFAULT_REPULSION_EXPONENT

    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for source in space.entities.by_components(PositionComponent, RepulsionComponent):
            source_position: PositionComponent = source.get(PositionComponent)
            source_repulsion: RepulsionComponent = source.get(RepulsionComponent)

            for entity in space.entities.by_components(PositionComponent, VelocityComponent):
                if entity.id == source.id:
                    continue

                position: PositionComponent = entity.get(PositionComponent)
                velocity: VelocityComponent = entity.get(VelocityComponent)

                if isinstance(velocity.velocity, Binding):
                    continue

                distance: Vector = resolve(position.position) - resolve(source_position.position)
                relative_distance: int | float = distance.length / resolve(source_repulsion.max_distance)

                if relative_distance >= 1:
                    continue

                velocity.velocity += distance.normalized * (1 - relative_distance) ** resolve(self._repulsion_exponent) * resolve(source_repulsion.max_repulsion) * delta
