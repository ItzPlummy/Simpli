from simpli import Simpli
from simpli.counters import Time
from simpli.spaces import Space
from simpli.systems import TickSystem


class TestSystem(TickSystem):
    @classmethod
    def tag(cls) -> str:
        return "test"

    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        time: Time | None = space.resources.get(Time)

        if time is None:
            return

        print(f"Tick: {time.tick}, delta: {delta}")


class Example(Simpli):
    ...


def main() -> None:
    e = Example()
    e.space.systems.add(TestSystem())
    e.start()


if __name__ == '__main__':
    main()
