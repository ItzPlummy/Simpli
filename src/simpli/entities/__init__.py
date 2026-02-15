from typing import TYPE_CHECKING, Any, Sequence, Tuple, Type, Dict

from ._entity import AbstractEntity, Entity
from ._entity_holder import AbstractEntityHolder, EntityHolder
from simpli.components import Component, PositionComponent, CircleComponent, ShapeComponent, VelocityComponent, \
    AirFrictionComponent, RepulsionComponent
from simpli.utils import Vector, Color, Value
from simpli.shapes import Circle
from simpli.enums import LayerGroup

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any


class CircleEntity(Entity):
    def __init__(
            self,
            position: Vector = Vector.zero(),
            radius: float = 50,
            color: Color = Color.black(),
            *,
            app: Simpli,
            name: str | None = None,
            parent: AbstractEntity | None = None,
            children: Sequence[AbstractEntity] | None = None,
            components: Sequence[Tuple[Type[Component], Dict[str, Any]]] | None = None,
    ) -> None:
        super().__init__(
            app=app,
            name=name,
            parent=parent,
            children=[
                app.entities.new(
                    name="main_circle",
                    components=[
                        (ShapeComponent, {"shape": app.shapes.new(
                            Circle,
                            layer_group_getter=lambda: LayerGroup.GEOMETRY,
                            position_getter=lambda: self.components.get(PositionComponent).position,
                            radius_getter=lambda: self.components.get(CircleComponent).radius,
                            color_getter=lambda: self.components.get(CircleComponent).color,
                        )})
                    ],
                ),
                app.entities.new(
                    name="shadow_circle",
                    components=[
                        (ShapeComponent, {"shape": app.shapes.new(
                            Circle,
                            layer_group_getter=lambda: LayerGroup.BACKGROUND,
                            position_getter=lambda: self.components.get(PositionComponent).position + Vector(5, -5),
                            radius_getter=lambda: self.components.get(CircleComponent).radius,
                            color_getter=Color.shadow,
                        )})
                    ],
                ),
                *(children or []),
            ],
            components=[
                (PositionComponent, {"position": position}),
                (CircleComponent, {"radius": radius, "color": color}),
                *(components or []),
            ],
        )


class RepulsiveCircleEntity(CircleEntity):
    def __init__(
            self,
            position: Vector = Vector.zero(),
            radius: float = 50,
            color: Color = Color.black(),
            initial_velocity: Vector = Vector.zero(),
            repulsion_strength: float = 1,
            *,
            app: Simpli,
            name: str | None = None,
            parent: AbstractEntity | None = None,
            children: Sequence[AbstractEntity] | None = None,
            components: Sequence[Tuple[Type[Component], Dict[str, Any]]] | None = None,
    ) -> None:
        super().__init__(
            position,
            radius,
            color,
            app=app,
            name=name,
            parent=parent,
            children=children or [],
            components=[
                (VelocityComponent, {"velocity": initial_velocity}),
                (AirFrictionComponent, {}),
                (RepulsionComponent, {
                    "repulsion_strength": repulsion_strength,
                    "repulsion_range": Value(lambda: self.components.get(CircleComponent).radius * 2.5)
                }),
                *(components or []),
            ],
        )


__all__ = [
    AbstractEntity,
    Entity,
    AbstractEntityHolder,
    EntityHolder,
]
