from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Iterable

from simpli.components import Component

if TYPE_CHECKING:
    from simpli.spaces import Space
else:
    Space = Any


class Entity(ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        ...

    @property
    @abstractmethod
    def space(self) -> Space:
        ...

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        ...

    @property
    @abstractmethod
    def parent(self) -> Entity:
        ...

    @property
    @abstractmethod
    def children(self) -> Iterable[Entity]:
        ...

    @abstractmethod
    def add(
            self,
            component: Component,
    ) -> None:
        ...

    @abstractmethod
    def get[T](
            self,
            component: type[T],
    ) -> T:
        ...

    @abstractmethod
    def find[T](
            self,
            component: type[T],
    ) -> T | None:
        ...

    @abstractmethod
    def has(
            self,
            component: type[Component],
    ) -> bool:
        ...

    @abstractmethod
    def remove(
            self,
            component: type[Component],
    ) -> None:
        ...

    @abstractmethod
    def destroy(self) -> None:
        ...
