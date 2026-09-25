from simpli import Simpli
from simpli.components.motion import Position, Velocity
from simpli.systems.motion import VelocitySystem
from simpli.utils import Vector


class Example(Simpli):
    ...


def main() -> None:
    e = Example()
    e.space.systems.add(VelocitySystem())
    e.space.entities.create(
        Position(
            position=Vector.zero()
        ),
        Velocity(
            velocity=Vector(1, 0),
        )
    )
    e.start()


if __name__ == '__main__':
    main()
