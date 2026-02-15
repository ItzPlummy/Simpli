from typing import TYPE_CHECKING, Any, Sequence, Tuple, Type, Dict

from ._entity import AbstractEntity, Entity
from ._entity_holder import AbstractEntityHolder, EntityHolder
from simpli.components import Component, PositionComponent, CircleComponent, ShapeComponent
from simpli.utils import Vector, Color
from simpli.shapes import Circle

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
                            position_getter=lambda: self.components.get(PositionComponent).position + Vector(5, -5),
                            radius_getter=lambda: self.components.get(CircleComponent).radius,
                            color_getter=Color.shadow,
                        )})
                    ],
                ),
            ],
            components=[
                (PositionComponent, {"position": position}),
                (CircleComponent, {"radius": radius, "color": color}),
                *(components or []),
            ],
        )


__all__ = [
    AbstractEntity,
    Entity,
    AbstractEntityHolder,
    EntityHolder,
]
