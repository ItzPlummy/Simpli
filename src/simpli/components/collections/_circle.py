from simpli.components.collections._collection import ComponentCollection
from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.components.shape import CircleComponent
from simpli.utils import Vector, Color


class StaticCircleEntity(ComponentCollection):
    def __init__(
            self,
            position: Vector,
            radius: int | float,
            *,
            color: Color | None = None,
            layer: int | None = None,
            is_visible: bool | None = None,
            offset: Vector | None = None,
    ) -> None:
        super().__init__(
            PositionComponent(
                position=position,
            ),
            CircleComponent(
                color=color if color is not None else Color.random(),
                layer=layer if layer is not None else 0,
                is_visible=is_visible if is_visible is not None else True,
                offset=offset if offset is not None else Vector.zero(),
                radius=radius,
            ),
        )


class DynamicCircleEntity(ComponentCollection):
    def __init__(
            self,
            position: Vector,
            radius: int | float,
            *,
            color: Color | None = None,
            layer: int | None = None,
            is_visible: bool | None = None,
            offset: Vector | None = None,
    ) -> None:
        super().__init__(
            PositionComponent(
                position=position,
            ),
            VelocityComponent(),
            CircleComponent(
                color=color if color is not None else Color.random(),
                layer=layer if layer is not None else 0,
                is_visible=is_visible if is_visible is not None else True,
                offset=offset if offset is not None else Vector.zero(),
                radius=radius,
            ),
        )
