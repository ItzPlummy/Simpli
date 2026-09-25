from abc import ABC, abstractmethod
from typing import Iterable, TYPE_CHECKING, Any

from simpli.components import Component
from simpli.entities._entity import Entity

if TYPE_CHECKING:
    from simpli.structures import Structure
else:
    Structure = Any


class EntityHolder(ABC):
    @abstractmethod
    def create(
            self,
            *components: Component,
    ) -> Entity:
        ...

    @abstractmethod
    def place(
            self,
            structure: Structure,
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
    def get_parent(
            self,
            entity_id: int,
    ) -> Entity | None:
        ...

    @abstractmethod
    def get_children(
            self,
            entity_id: int,
    ) -> Iterable[Entity]:
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

    @abstractmethod
    def attach_to(
            self,
            parent_id: int,
            child_id: int,
    ) -> None:
        ...

    @abstractmethod
    def detach(
            self,
            child_id: int,
    ) -> None:
        ...

    def attach_children(
            self,
            parent_id: int,
            *children: int,
    ) -> None:
        for child_id in children:
            self.attach_to(parent_id, child_id)

    def detach_child(
            self,
            parent_id: int,
            child_id: int,
    ) -> None:
        if self.get_parent(child_id) == parent_id:
            self.detach(child_id)

    @property
    @abstractmethod
    def all(self) -> Iterable[Entity]:
        ...

    @property
    @abstractmethod
    def count(self) -> int:
        ...

    def __iter__(self) -> Iterable[Entity]:
        return self.all

    def __len__(self) -> int:
        return self.count
