from simpli.components.collections._collection import ComponentCollection
from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.components.visual.shape import CircleComponent
from simpli.utils import Vector, Color, Resolvable


class StaticCircleEntity(ComponentCollection):
    def __init__(
            self,
            position: Resolvable[Vector],
            radius: Resolvable[int | float],
            *,
            is_visible: Resolvable[bool] | None = None,
            layer: Resolvable[int] | None = None,
            offset: Resolvable[Vector] | None = None,
            color: Resolvable[Color] | None = None,
    ) -> None:
        super().__init__(
            PositionComponent(
                position=position,
            ),
            CircleComponent(
                radius=radius,
                is_visible=is_visible if is_visible is not None else True,
                layer=layer if layer is not None else 0,
                offset=offset if offset is not None else Vector.zero(),
                color=color if color is not None else Color.random(),
            ),
        )


class DynamicCircleEntity(ComponentCollection):
    def __init__(
            self,
            position: Resolvable[Vector],
            radius: Resolvable[int | float],
            *,
            is_visible: Resolvable[bool] | None = None,
            layer: Resolvable[int] | None = None,
            offset: Resolvable[Vector] | None = None,
            color: Resolvable[Color] | None = None,
    ) -> None:
        super().__init__(
            PositionComponent(
                position=position,
            ),
            VelocityComponent(),
            CircleComponent(
                radius=radius,
                is_visible=is_visible if is_visible is not None else True,
                layer=layer if layer is not None else 0,
                offset=offset if offset is not None else Vector.zero(),
                color=color if color is not None else Color.random(),
            ),
        )
