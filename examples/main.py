from simpli import Simpli
from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.spaces import Space
from simpli.systems import StartSystem
from simpli.systems.motion import VelocitySystem
from simpli.utils import Vector


class SetupSystem(StartSystem):
    @classmethod
    def tag(cls) -> str:
        return "setup"

    def on_start(self, space: Space) -> None:
        space.entities.create(
            PositionComponent(
                position=Vector.zero(),
            ),
            VelocityComponent(
                velocity=Vector(1, 0),
            )
        )


class Example(Simpli):
    SYSTEMS = [
        SetupSystem(),
        VelocitySystem(),
    ]


def main() -> None:
    example = Example()
    example.start()


if __name__ == '__main__':
    main()
