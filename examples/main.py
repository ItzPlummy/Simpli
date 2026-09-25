from random import randint

from simpli import Simpli
from simpli.components.collections import DynamicCircleEntity
from simpli.components.motion import VelocityComponent, PositionComponent
from simpli.entities import Entity
from simpli.enums import MouseButton
from simpli.spaces import Space
from simpli.systems import StartSystem, TickSystem, MouseClickSystem
from simpli.systems.motion import AirResistanceSystem, VelocitySystem, GravitySystem
from simpli.utils import Vector


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
        entity: Entity = space.entities.create_collection(
            DynamicCircleEntity(position, randint(20, 50))
        )

        entity.get(VelocityComponent).velocity += Vector.random() * 200


class BounceSystem(TickSystem):
    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for entity in space.entities.by_components(PositionComponent, VelocityComponent):
            position: PositionComponent = entity.get(PositionComponent)
            velocity: VelocityComponent = entity.get(VelocityComponent)

            if position.position.y < -300:
                position.position = position.position.with_y(-300)
                velocity.velocity = velocity.velocity.with_y(velocity.velocity.y * -1)


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
        BounceSystem(),
        GravitySystem(),
        AirResistanceSystem(),
        VelocitySystem(),
        DebugSystem(),
    ]


def main() -> None:
    example = Example()
    example.start()


if __name__ == '__main__':
    main()
