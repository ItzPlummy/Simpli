from simpli.resources import ResourceHolder, DefaultResourceHolder
from simpli.spaces._space import Space
from simpli.systems import SystemHolder, DefaultSystemHolder, TickSystem, FrameSystem


class DefaultSpace(Space):
    def __init__(self) -> None:
        self._systems: SystemHolder = DefaultSystemHolder()
        self._resources: ResourceHolder = DefaultResourceHolder()

    @property
    def systems(self) -> SystemHolder:
        return self._systems

    @property
    def resources(self) -> ResourceHolder:
        return self._resources

    def on_tick(
            self,
            delta: int | float,
    ) -> None:
        for system in self.systems.of_kind(TickSystem):
            system.on_tick(self, delta)

    def on_frame(
            self,
            alpha: int | float,
    ) -> None:
        for system in self.systems.of_kind(FrameSystem):
            system.on_frame(self, alpha)
