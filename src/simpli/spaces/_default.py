from simpli.resources import ResourceHolder, DefaultResourceHolder
from simpli.spaces._space import Space


class DefaultSpace(Space):
    def __init__(self) -> None:
        self._resources: ResourceHolder = DefaultResourceHolder()

    @property
    def resources(self) -> ResourceHolder:
        return self._resources

    def step(self, delta: int | float) -> None:
        ...
