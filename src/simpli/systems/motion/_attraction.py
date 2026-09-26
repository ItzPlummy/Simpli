from simpli.components.motion import AttractionComponent, VelocityComponent, PositionComponent
from simpli.spaces import Space
from simpli.systems import TickSystem
from simpli.utils import Vector, resolve, Supplier, Resolvable


class AttractionSystem(TickSystem):
    _DEFAULT_ATTRACTION_EXPONENT: int | float = 3

    def __init__(
            self,
            *,
            attraction_exponent: Resolvable[int | float] | None = None,
    ) -> None:
        self._attraction_exponent: Resolvable[int | float] = attraction_exponent if attraction_exponent is not None else self._DEFAULT_ATTRACTION_EXPONENT

    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for source in space.entities.by_components(PositionComponent, AttractionComponent):
            source_position: PositionComponent = source.get(PositionComponent)
            source_attraction: AttractionComponent = source.get(AttractionComponent)

            for entity in space.entities.by_components(PositionComponent, VelocityComponent):
                if entity.id == source.id:
                    continue

                position: PositionComponent = entity.get(PositionComponent)
                velocity: VelocityComponent = entity.get(VelocityComponent)

                if isinstance(velocity.velocity, Supplier):
                    continue

                distance: Vector = resolve(position.position) - resolve(source_position.position)
                relative_distance: int | float = distance.length / resolve(source_attraction.max_distance)

                if relative_distance >= 1:
                    continue

                velocity.velocity -= distance.normalized * (1 - relative_distance) ** resolve(self._attraction_exponent) * resolve(source_attraction.max_attraction) * delta
