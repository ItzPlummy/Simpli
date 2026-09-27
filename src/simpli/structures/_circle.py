from simpli.components import Component
from simpli.components.effect import BouncyAppearanceEffectComponent
from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.components.visual.shape import CircleComponent
from simpli.counters import Time
from simpli.entities import Entity
from simpli.spaces import Space
from simpli.structures._structure import Structure
from simpli.utils import Resolvable, Vector, Color, Binding, resolve


class Circle(Structure):
    def __init__(
            self,
            position: Resolvable[Vector],
            radius: Resolvable[int | float],
            *,
            is_dynamic: bool = False,
            has_shadow: bool = True,
            has_bouncy_appearance: bool = True,
            is_visible: Resolvable[bool] | None = None,
            is_shadow_visible: Resolvable[bool] | None = None,
            layer: Resolvable[int] | None = None,
            offset: Resolvable[Vector] | None = None,
            shadow_offset: Resolvable[Vector] | None = None,
            color: Resolvable[Color] | None = None,
            shadow_color: Resolvable[Color] | None = None,
            bouncy_appearance_amplitude: Resolvable[int | float] | None = None,
            bouncy_appearance_frequency: Resolvable[int | float] | None = None,
            bouncy_appearance_duration: Resolvable[int | float] | None = None,
    ) -> None:
        self._position: Resolvable[Vector] = position
        self._radius: Resolvable[int | float] = radius
        self._is_dynamic: bool = is_dynamic
        self._has_shadow: bool = has_shadow
        self._has_bouncy_appearance: bool = has_bouncy_appearance
        self._is_visible: Resolvable[bool] = is_visible if is_visible is not None else True
        self._is_shadow_visible: Resolvable[bool] = is_shadow_visible if is_shadow_visible is not None else True
        self._layer: Resolvable[int] = layer if layer is not None else 0
        self._offset: Resolvable[Vector] = offset if offset is not None else Vector.zero()
        self._shadow_offset: Resolvable[Vector] = shadow_offset if shadow_offset is not None else Vector(7.5, -7.5)
        self._color: Resolvable[Color] = color if color is not None else Color.random()
        self._shadow_color: Resolvable[Color] = shadow_color if shadow_color is not None else Color.shadow()
        self._bouncy_appearance_amplitude: Resolvable[int | float] = bouncy_appearance_amplitude if bouncy_appearance_amplitude is not None else 0.25
        self._bouncy_appearance_frequency: Resolvable[int | float] = bouncy_appearance_frequency if bouncy_appearance_frequency is not None else 1.25
        self._bouncy_appearance_duration: Resolvable[int | float] = bouncy_appearance_duration if bouncy_appearance_duration is not None else 120

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

        components: list[Component] = [position_component, circle_component]

        if self._is_dynamic:
            components.append(VelocityComponent())
        if self._has_bouncy_appearance:
            components.append(
                BouncyAppearanceEffectComponent(
                    start_tick=space.resources.get(Time).tick,
                    amplitude=self._bouncy_appearance_amplitude,
                    frequency=self._bouncy_appearance_frequency,
                    duration=self._bouncy_appearance_duration,
                )
            )

        circle: Entity = space.entities.create(*components)

        if self._has_shadow:
            shadow_position: PositionComponent = PositionComponent(
                position=Binding(lambda: resolve(position_component.position)),
            )

            shadow_circle: CircleComponent = CircleComponent(
                radius=Binding(lambda: resolve(circle_component.radius)),
                is_visible=Binding(lambda: resolve(circle_component.is_visible)),
                layer=Binding(lambda: resolve(circle_component.layer) - 1),
                offset=Binding(lambda: resolve(circle_component.offset) + resolve(self._shadow_offset)),
                color=self._shadow_color,
            )

            shadow_components: list[Component] = [shadow_position, shadow_circle]

            if self._has_bouncy_appearance:
                shadow_components.append(
                    BouncyAppearanceEffectComponent(
                        start_tick=space.resources.get(Time).tick,
                        amplitude=self._bouncy_appearance_amplitude,
                        frequency=self._bouncy_appearance_frequency,
                        duration=self._bouncy_appearance_duration,
                    )
                )

            circle.attach_children(space.entities.create(*shadow_components).id)

        return circle
