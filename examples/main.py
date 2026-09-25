from simpli import Simpli
from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.components.shape import CircleComponent
from simpli.entities import Entity
from simpli.spaces import Space
from simpli.systems import StartSystem, TickSystem
from simpli.utils import Vector, Color

entity: Entity


class SetupSystem(StartSystem):
    def on_start(self, space: Space) -> None:
        global entity

        entity = space.entities.create(
            PositionComponent(
                position=Vector.zero(),
            ),
            VelocityComponent(
                velocity=Vector(50, 0),
            ),
            CircleComponent(
                color=Color.black(),
                radius=50,
            ),
        )


class DebugSystem(TickSystem):
    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        print(entity.get(PositionComponent).position)


class Example(Simpli):
    SYSTEMS = [
        SetupSystem(),
        DebugSystem(),
    ]


def main() -> None:
    example = Example()
    example.start()


if __name__ == '__main__':
    main()
