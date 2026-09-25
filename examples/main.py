from simpli import Simpli
from simpli.components.motion import PositionComponent, VelocityComponent
from simpli.systems.motion import VelocitySystem
from simpli.utils import Vector


class Example(Simpli):
    ...


def main() -> None:
    e = Example()
    e.space.systems.add(VelocitySystem())
    e.space.entities.create(
        PositionComponent(
            position=Vector.zero()
        ),
        VelocityComponent(
            velocity=Vector(1, 0),
        )
    )
    e.start()


if __name__ == '__main__':
    main()
