from simpli.entities import EntityHolder, DefaultEntityHolder
from simpli.resources import ResourceHolder, DefaultResourceHolder
from simpli.spaces._space import Space
from simpli.systems import SystemHolder, DefaultSystemHolder, TickSystem, FrameSystem, StartSystem


class DefaultSpace(Space):
    def __init__(self) -> None:
        self._entities: EntityHolder = DefaultEntityHolder(self)
        self._systems: SystemHolder = DefaultSystemHolder()
        self._resources: ResourceHolder = DefaultResourceHolder()

    @property
    def entities(self) -> EntityHolder:
        return self._entities

    @property
    def systems(self) -> SystemHolder:
        return self._systems

    @property
    def resources(self) -> ResourceHolder:
        return self._resources

    def on_start(self) -> None:
        for system in self.systems.of_kind(StartSystem):
            system.on_start(self)

    def on_tick(
            self,
            delta: int | float,
    ) -> None:
        for system in self.systems.of_kind(TickSystem):
            system.on_tick(self, delta)

        self.entities.flush()

    def on_frame(
            self,
            alpha: int | float,
    ) -> None:
        for system in self.systems.of_kind(FrameSystem):
            system.on_frame(self, alpha)
