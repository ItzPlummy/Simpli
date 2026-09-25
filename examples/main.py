from random import randint

from simpli import Simpli
from simpli.components.collections import DynamicCircleEntity
from simpli.enums import MouseButton
from simpli.spaces import Space
from simpli.systems import StartSystem, TickSystem, MouseClickSystem
from simpli.systems.motion import AirResistanceSystem, VelocitySystem, GravitySystem
from simpli.utils import Vector, Supplier

_gravity_acceleration: int | float = 0


class SetupSystem(StartSystem):
    def on_start(self, space: Space) -> None:
        ...


class CircleSpawnSystem(MouseClickSystem):
    def on_mouse_click(
            self,
            space: Space,
            position: Vector,
            screen_position: Vector,
            mouse_button: MouseButton,
    ) -> None:
        space.entities.create_collection(
            DynamicCircleEntity(position, randint(20, 50))
        )


class GravityIncreasementSystem(TickSystem):
    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        global _gravity_acceleration
        _gravity_acceleration += delta * 1000


class DebugSystem(TickSystem):
    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        ...


class Example(Simpli):
    SYSTEMS = [
        SetupSystem(),
        CircleSpawnSystem(),
        GravityIncreasementSystem(),
        GravitySystem(
            acceleration=Supplier(lambda: Vector(0, -_gravity_acceleration))
        ),
        AirResistanceSystem(),
        VelocitySystem(),
        DebugSystem(),
    ]


def main() -> None:
    example = Example()
    example.start()


if __name__ == '__main__':
    main()
