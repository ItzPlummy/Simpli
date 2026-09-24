from simpli import Simpli
from simpli.components import Component
from simpli.spaces import Space
from simpli.systems import TickSystem


class Position(Component):
    x: int | float
    y: int | float


class GravitySystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "gravity"

    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        for entity in space.entities.by_component(Position):
            entity.get(Position).x += 0.01
            print(entity.get(Position).x)


class Example(Simpli):
    ...


def main() -> None:
    e = Example()
    e.space.systems.add(GravitySystem())
    e.space.entities.create(Position(x=0, y=0))
    e.start()


if __name__ == '__main__':
    main()
