from random import randint

from simpli import Simpli
from simpli.enums import MouseButton
from simpli.spaces import Space
from simpli.structures import Circle
from simpli.systems import MouseClickSystem
from simpli.systems.motion import AirResistanceSystem, VelocitySystem
from simpli.utils import Vector


class CircleSpawnSystem(MouseClickSystem):
    def on_mouse_click(
            self,
            space: Space,
            position: Vector,
            screen_position: Vector,
            mouse_button: MouseButton,
    ) -> None:
        space.entities.place(
            Circle(
                position,
                randint(20, 50),
                is_dynamic=True,
            )
        )


class Example(Simpli):
    SYSTEMS = [
        CircleSpawnSystem(),
        AirResistanceSystem(),
        VelocitySystem(),
    ]


def main() -> None:
    Example().start()


if __name__ == '__main__':
    main()
