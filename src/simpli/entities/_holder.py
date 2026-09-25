from abc import ABC, abstractmethod
from typing import Iterable

from simpli.components import Component
from simpli.components.collections import ComponentCollection
from simpli.entities._entity import Entity


class EntityHolder(ABC):
    @abstractmethod
    def create(
            self,
            *components: Component,
    ) -> Entity:
        ...

    @abstractmethod
    def create_collection(
            self,
            collection: ComponentCollection,
    ) -> Entity:
        ...

    @abstractmethod
    def get(
            self,
            entity_id: int,
    ) -> Entity:
        ...

    @abstractmethod
    def find(
            self,
            entity_id: int,
    ) -> Entity | None:
        ...

    @abstractmethod
    def has(
            self,
            entity_id: int,
    ) -> bool:
        ...

    @abstractmethod
    def is_alive(
            self,
            entity_id: int,
    ) -> bool:
        ...

    @abstractmethod
    def destroy(
            self,
            entity_id: int,
    ) -> None:
        ...

    @abstractmethod
    def add_component(
            self,
            entity_id: int,
            component: Component,
    ) -> None:
        ...

    @abstractmethod
    def get_component[T: Component](
            self,
            entity_id: int,
            component: type[T],
    ) -> T:
        ...

    @abstractmethod
    def find_component[T: Component](
            self,
            entity_id: int,
            component: type[T],
    ) -> T | None:
        ...

    @abstractmethod
    def get_components(
            self,
            entity_id: int,
    ) -> Iterable[Component]:
        ...

    @abstractmethod
    def has_component(
            self,
            entity_id: int,
            component: type[Component],
    ) -> bool:
        ...

    @abstractmethod
    def remove_component(
            self,
            entity_id: int,
            component: type[Component],
    ) -> None:
        ...

    @abstractmethod
    def by_component(
            self,
            component: type[Component],
    ) -> Iterable[Entity]:
        ...

    @abstractmethod
    def by_components(
            self,
            *components: type[Component],
    ) -> Iterable[Entity]:
        ...

    @abstractmethod
    def flush(self) -> None:
        ...

    @property
    @abstractmethod
    def count(self) -> int:
        ...
