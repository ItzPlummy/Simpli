from typing import TYPE_CHECKING, Any, Sequence, Tuple, Type, Dict

from simpli.components import Component, PositionComponent, CircleComponent, ShapeComponent, VelocityComponent, \
    AirFrictionComponent, RepulsionComponent, AttractionComponent
from simpli.enums import LayerGroup
from simpli.shapes import Circle, BackgroundRectangle
from simpli.utils import Vector, Color, Value
from ._entity import AbstractEntity, Entity
from ._entity_holder import AbstractEntityHolder, EntityHolder

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any


class CircleEntity(Entity):
    def __init__(
            self,
            position: Vector | None = None,
            radius: float | None = None,
            color: Color | None = None,
            *,
            app: Simpli,
            name: str | None = None,
            parent: AbstractEntity | None = None,
            components: Sequence[Tuple[Type[Component], Dict[str, Any]]] | None = None,
    ) -> None:
        super().__init__(
            app=app,
            name=name,
            parent=parent,
            components=[
                (PositionComponent, {"position": position or Vector.zero()}),
                (CircleComponent, {"radius": radius or 50, "color": color or Color.random()}),
                *(components or []),
            ],
        )

        self.set_child(
            app.entities.new(
                name="main_circle",
                components=[
                    (ShapeComponent, {"shape": app.shapes.new(
                        Circle,
                        position=Value(lambda: self.components.get(PositionComponent).position),
                        radius=Value(lambda: self.components.get(CircleComponent).radius),
                        color=Value(lambda: self.components.get(CircleComponent).color),
                    )})
                ],
            ),
        )

        self.set_child(
            app.entities.new(
                name="shadow_circle",
                components=[
                    (ShapeComponent, {"shape": app.shapes.new(
                        Circle,
                        layer_group=LayerGroup.SHADOW,
                        position=Value(lambda: self.components.get(PositionComponent).position + Vector(5, -5)),
                        radius=Value(lambda: self.components.get(CircleComponent).radius),
                        color=Color.shadow(),
                    )})
                ],
            ),
        )


class CellEntity(CircleEntity):
    def __init__(
            self,
            position: Vector | None = None,
            radius: float | None = None,
            color: Color | None = None,
            initial_velocity: Vector | None = None,
            attraction_strength: float | None = None,
            repulsion_strength: float | None = None,
            *,
            app: Simpli,
            name: str | None = None,
            parent: AbstractEntity | None = None,
            components: Sequence[Tuple[Type[Component], Dict[str, Any]]] | None = None,
    ) -> None:
        super().__init__(
            position,
            radius,
            color,
            app=app,
            name=name,
            parent=parent,
            components=[
                (VelocityComponent, {"velocity": initial_velocity or Vector.zero()}),
                (AirFrictionComponent, {}),
                (AttractionComponent, {
                    "strength": attraction_strength or 0.25,
                    "range": Value(lambda: self.components.get(CircleComponent).radius * 10),
                    "power_factor": 0.25,
                }),
                (RepulsionComponent, {
                    "strength": repulsion_strength or 2,
                    "range": Value(lambda: self.components.get(CircleComponent).radius * 2.5),
                    "power_factor": 1.25,
                }),
                *(components or []),
            ],
        )


class BackgroundEntity(Entity):
    def __init__(self, *, app: Simpli) -> None:
        super().__init__(
            app=app,
            name="background_rectangle",
            components=[
                (ShapeComponent, {"shape": app.shapes.new(
                    BackgroundRectangle
                )})
            ]
        )


__all__ = [
    AbstractEntity,
    Entity,
    AbstractEntityHolder,
    EntityHolder,
]
