from random import randint

from simpli import Simpli
from simpli.components.motion import RepulsionComponent, AttractionComponent, VelocityComponent
from simpli.components.visual.shape import CircleComponent
from simpli.entities import Entity
from simpli.enums import MouseButton
from simpli.spaces import Space
from simpli.structures import Circle
from simpli.systems import MouseClickSystem
from simpli.systems.motion import AirResistanceSystem, VelocitySystem, RepulsionSystem, AttractionSystem
from simpli.utils import Vector, Binding, resolve, Color

_MAX_REGISTERED_VELOCITY: int | float = 500


def _get_relative_velocity(velocity: Vector) -> int | float:
    return min(1, velocity.length / _MAX_REGISTERED_VELOCITY)


class CircleSpawnSystem(MouseClickSystem):
    def on_mouse_click(
            self,
            space: Space,
            position: Vector,
            screen_position: Vector,
            mouse_button: MouseButton,
    ) -> None:
        entity: Entity = space.entities.place(
            Circle(
                position,
                randint(35, 50),
                is_dynamic=True,
            )
        )

        velocity: VelocityComponent = entity.get(VelocityComponent)
        circle: CircleComponent = entity.get(CircleComponent)

        circle.color = Binding(
            lambda: Color(
                red=_get_relative_velocity(resolve(velocity.velocity)),
                blue=_get_relative_velocity(resolve(velocity.velocity)),
            )
        )

        entity.add(
            RepulsionComponent(
                max_repulsion=Binding(lambda: resolve(circle.radius) * 150),
                max_distance=Binding(lambda: resolve(circle.radius) * 5),
            )
        )
        entity.add(
            AttractionComponent(
                max_attraction=Binding(lambda: resolve(circle.radius) * 10),
                max_distance=Binding(lambda: resolve(circle.radius) * 20),
            )
        )


class Example(Simpli):
    SYSTEMS = [
        CircleSpawnSystem(),
        RepulsionSystem(),
        AttractionSystem(),
        AirResistanceSystem(),
        VelocitySystem(),
    ]


def main() -> None:
    Example().start()


if __name__ == '__main__':
    main()
