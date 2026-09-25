from simpli.components import Component
from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.components.visual.shape import CircleComponent
from simpli.entities import Entity
from simpli.spaces import Space
from simpli.structures._structure import Structure
from simpli.utils import Resolvable, Vector, Color, Supplier, resolve


class Circle(Structure):
    def __init__(
            self,
            position: Resolvable[Vector],
            radius: Resolvable[int | float],
            *,
            is_dynamic: bool = False,
            has_shadow: bool = True,
            is_visible: Resolvable[bool] | None = None,
            is_shadow_visible: Resolvable[bool] | None = None,
            layer: Resolvable[int] | None = None,
            offset: Resolvable[Vector] | None = None,
            shadow_offset: Resolvable[Vector] | None = None,
            color: Resolvable[Color] | None = None,
            shadow_color: Resolvable[Color] | None = None,
    ) -> None:
        self._position: Resolvable[Vector] = position
        self._radius: Resolvable[int | float] = radius
        self._is_dynamic: bool = is_dynamic
        self._has_shadow: bool = has_shadow
        self._is_visible: Resolvable[bool] = is_visible if is_visible is not None else True
        self._is_shadow_visible: Resolvable[bool] = is_shadow_visible if is_shadow_visible is not None else True
        self._layer: Resolvable[int] = layer if layer is not None else 0
        self._offset: Resolvable[Vector] = offset if offset is not None else Vector.zero()
        self._shadow_offset: Resolvable[Vector] = shadow_offset if shadow_offset is not None else Vector(7.5, -7.5)
        self._color: Resolvable[Color] = color if color is not None else Color.random()
        self._shadow_color: Resolvable[Color] = shadow_color if shadow_color is not None else Color.shadow()

    def place(
            self,
            space: Space,
    ) -> Entity:
        position_component: PositionComponent = PositionComponent(
            position=self._position,
        )

        circle_component: CircleComponent = CircleComponent(
            radius=self._radius,
            is_visible=self._is_visible,
            layer=self._layer,
            offset=self._offset,
            color=self._color,
        )

        components: list[Component] = [position_component, circle_component] if not self._is_dynamic else [position_component, VelocityComponent(), circle_component]

        circle: Entity = space.entities.create(*components)

        circle.attach_children(
            space.entities.create(
                PositionComponent(
                    position=Supplier(lambda: resolve(position_component.position)),
                ),
                CircleComponent(
                    radius=Supplier(lambda: resolve(circle_component.radius)),
                    is_visible=Supplier(lambda: resolve(circle_component.is_visible)),
                    layer=Supplier(lambda: resolve(circle_component.layer) - 1),
                    offset=Supplier(lambda: resolve(circle_component.offset) + resolve(self._shadow_offset)),
                    color=self._shadow_color,
                ),
            ).id
        )

        return circle
