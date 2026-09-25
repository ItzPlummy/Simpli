from collections import defaultdict
from itertools import count
from typing import Iterable, TYPE_CHECKING, Any

from simpli.components import Component
from simpli.components.collections import ComponentCollection
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

    @property
    def parent(self) -> Entity | None:
        return self.space.entities.get_parent(self._id)

    @property
    def children(self) -> Iterable[Entity]:
        return self.space.entities.get_children(self._id)

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

    def attach_to(
            self,
            parent_id: int,
    ) -> None:
        self.space.entities.attach_to(parent_id, self._id)

    def detach(self) -> None:
        self.space.entities.detach(self._id)

    def attach_children(
            self,
            *children: int,
    ) -> None:
        self.space.entities.attach_children(self._id, *children)

    def detach_child(
            self,
            child_id: int,
    ) -> None:
        self.space.entities.detach_child(self._id, child_id)


class DefaultEntityHolder(EntityHolder):
    def __init__(
            self,
            space: Space,
    ) -> None:
        self._space: Space = space

        self._ids: count[int] = count(1)

        self._entities: dict[type[Component], dict[int, Component]] = defaultdict[type[Component], dict[int, Component]](dict)
        self._components: dict[int, set[type[Component]]] = defaultdict[int, set[type[Component]]](set)

        self._parents: dict[int, int] = {}
        self._children: dict[int, set[int]] = defaultdict[int, set[int]](set)

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

        self._components[entity_id] = {type(component) for component in components}

        for component in components:
            self._entities[type(component)][entity_id] = component

        return DefaultEntity(entity_id, self._space)

    def create_collection(
            self,
            collection: ComponentCollection,
    ) -> Entity:
        return self.create(*collection())

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
        return entity_id in self._components

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
        self._components[entity_id].add(type(component))
        self._entities[type(component)][entity_id] = component

    def get_component[T: Component](
            self,
            entity_id: int,
            component: type[T],
    ) -> T:
        try:
            return self._entities[component][entity_id]
        except KeyError:
            raise RuntimeError("Unable to get component from entity")

    def find_component[T: Component](
            self,
            entity_id: int,
            component: type[T],
    ) -> T | None:
        try:
            return self._entities[component][entity_id]
        except KeyError:
            return None

    def get_components(
            self,
            entity_id: int,
    ) -> Iterable[Component]:
        for component_type in self._components[entity_id]:
            component: Component | None = self._entities[component_type].get(entity_id)

            if component is not None:
                yield component

    def has_component(
            self,
            entity_id: int,
            component: type[Component],
    ) -> bool:
        return component in self._components[entity_id]

    def remove_component(
            self,
            entity_id: int,
            component: type[Component],
    ) -> None:
        self._components.pop(entity_id, None)
        self._entities[component].pop(entity_id, None)

    def by_component(
            self,
            component: type[Component],
    ) -> Iterable[Entity]:
        for entity_id in self._entities[component]:
            yield DefaultEntity(entity_id, self._space)

    def by_components(
            self,
            *components: type[Component],
    ) -> Iterable[Entity]:
        entities: set[int] = set[int](self._components.keys())

        for component in components:
            entities &= self._entities[component].keys()

        for entity_id in entities:
            yield DefaultEntity(entity_id, self._space)

    def flush(self) -> None:
        for entity_id in self._destroyed:
            components: set[type[Component]] = self._components.pop(entity_id, set())

            for component in components:
                self._entities[component].pop(entity_id, None)

        self._destroyed.clear()

    def get_parent(
            self,
            entity_id: int,
    ) -> Entity | None:
        try:
            return DefaultEntity(self._parents[entity_id], self._space)
        except KeyError:
            return None

    def get_children(
            self,
            entity_id: int,
    ) -> Iterable[Entity]:
        for child_id in self._children[entity_id]:
            yield DefaultEntity(child_id, self._space)

    def attach_to(
            self,
            parent_id: int,
            child_id: int,
    ) -> None:
        self._parents[child_id] = parent_id
        self._children[parent_id].add(child_id)

    def detach(
            self,
            child_id: int,
    ) -> None:
        parent_id: int | None = self._parents.pop(child_id, None)

        if parent_id is not None:
            self._children[parent_id].discard(child_id)

    @property
    def count(self) -> int:
        return len(self._components)
