from collections import defaultdict
from itertools import count
from typing import Iterable, TYPE_CHECKING, Any

from simpli.components import Component
from simpli.entities._entity import Entity
from simpli.entities._holder import EntityHolder

if TYPE_CHECKING:
    from simpli.spaces import Space
else:
    Space = Any


class DefaultEntity(Entity):
    def __init__(
            self,
            entity_id: int,
            space: Space,
    ) -> None:
        self._id = entity_id
        self._space = space

    @property
    def id(self) -> int:
        return self._id

    @property
    def space(self) -> Space:
        return self._space

    @property
    def is_alive(self) -> bool:
        return self.space.entities.is_alive(self._id)

    def add(
            self,
            component: Component,
    ) -> None:
        self.space.entities.add_component(self._id, component)

    def get[T: Component](
            self,
            component: type[T],
    ) -> T:
        return self.space.entities.get_component(self._id, component)

    def find[T: Component](
            self,
            component: type[T],
    ) -> T | None:
        return self.space.entities.find_component(self._id, component)

    def has(
            self,
            component: type[Component],
    ) -> bool:
        return self.space.entities.has_component(self._id, component)

    def remove(
            self,
            component: type[Component],
    ) -> None:
        self.space.entities.remove_component(self._id, component)

    def destroy(self) -> None:
        self.space.entities.destroy(self._id)


class DefaultEntityHolder(EntityHolder):
    def __init__(
            self,
            space: Space,
    ) -> None:
        self._space: Space = space

        self._ids: count[int] = count(1)
        self._entities: dict[int, set[type[Component]]] = defaultdict[int, set[type[Component]]](set)
        self._components: dict[type[Component], dict[int, Component]] = defaultdict[type[Component], dict[int, Component]](dict)
        self._destroyed: set[int] = set()

    def create(
            self,
            *components: Component,
    ) -> Entity:
        entity_id: int

        for _ in range(10):
            entity_id = next(self._ids)
            if not self.has(entity_id): break
        else:
            raise RuntimeError("Unable to create entity")

        self._entities[entity_id] = {type(component) for component in components}

        for component in components:
            self._components[type(component)][entity_id] = component

        return DefaultEntity(entity_id, self._space)

    def get(
            self,
            entity_id: int,
    ) -> Entity:
        return DefaultEntity(entity_id, self._space)

    def find(
            self,
            entity_id: int,
    ) -> Entity | None:
        return None if not self.has(entity_id) else DefaultEntity(entity_id, self._space)

    def has(
            self,
            entity_id: int,
    ) -> bool:
        return entity_id in self._entities

    def is_alive(
            self,
            entity_id: int,
    ) -> bool:
        return self.has(entity_id) and entity_id not in self._destroyed

    def destroy(
            self,
            entity_id: int,
    ) -> None:
        self._destroyed.add(entity_id)

    def add_component(
            self,
            entity_id: int,
            component: Component,
    ) -> None:
        self._entities[entity_id].add(type(component))
        self._components[type(component)][entity_id] = component

    def get_component[T: Component](
            self,
            entity_id: int,
            component: type[T],
    ) -> T:
        try:
            return self._components[component][entity_id]
        except KeyError:
            raise RuntimeError("Unable to get component from entity")

    def find_component[T: Component](
            self,
            entity_id: int,
            component: type[T],
    ) -> T | None:
        try:
            return self._components[component][entity_id]
        except KeyError:
            return None

    def get_components(
            self,
            entity_id: int,
    ) -> Iterable[Component]:
        for component_type in self._entities[entity_id]:
            component: Component | None = self._components[component_type].get(entity_id)

            if component is not None:
                yield component

    def has_component(
            self,
            entity_id: int,
            component: type[Component],
    ) -> bool:
        return component in self._entities[entity_id]

    def remove_component(
            self,
            entity_id: int,
            component: type[Component],
    ) -> None:
        self._entities.pop(entity_id, None)
        self._components[component].pop(entity_id, None)

    def by_component(
            self,
            component: type[Component],
    ) -> Iterable[Entity]:
        for entity_id in self._components[component]:
            yield DefaultEntity(entity_id, self._space)

    def flush(self) -> None:
        for entity_id in self._destroyed:
            components: set[type[Component]] = self._entities.pop(entity_id, set())

            for component in components:
                self._components[component].pop(entity_id, None)

        self._destroyed.clear()
