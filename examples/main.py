from simpli import Simpli
from simpli.components.collections import StaticCircleEntity, DynamicCircleEntity
from simpli.components.motion import VelocityComponent
from simpli.spaces import Space
from simpli.systems import StartSystem, TickSystem
from simpli.utils import Vector


class SetupSystem(StartSystem):
    def on_start(self, space: Space) -> None:
        space.entities.create_collection(
            StaticCircleEntity(Vector.zero(), 50)
        )

        entity = space.entities.create_collection(
            DynamicCircleEntity(Vector.zero(), 40)
        )

        entity.get(VelocityComponent).velocity += Vector(300, 120)


class DebugSystem(TickSystem):
    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for entity in space.entities.by_component(VelocityComponent):
            print(entity.get(VelocityComponent))


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
