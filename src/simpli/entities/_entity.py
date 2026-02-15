from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING, Any, TypeVar, Iterable, Optional

from simpli.components import AbstractComponentHolder, ComponentHolder
from simpli.components import Component
from simpli.utils import Identifiable, AppDependant, AbstractIdentifierHolder, IdentifierHolder

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any

_CT = TypeVar("_CT", bound=Component)
_AET = TypeVar("_AET", bound="AbstractEntity")


class AbstractEntity(AppDependant, Identifiable, ABC):
    @property
    @abstractmethod
    def parent(self) -> Optional['AbstractEntity']:
        raise NotImplementedError

    @property
    @abstractmethod
    def children(self) -> Iterable['AbstractEntity']:
        raise NotImplementedError

    @property
    @abstractmethod
    def components(self) -> AbstractComponentHolder:
        raise NotImplementedError

    @abstractmethod
    def _set_parent(self, parent: Optional['AbstractEntity']) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_child(self, child_type: Type['AbstractEntity'], *args: Any, **kwargs: Any) -> 'AbstractEntity':
        raise NotImplementedError

    @abstractmethod
    def set_child(self, child: 'AbstractEntity') -> 'AbstractEntity':
        raise NotImplementedError

    @abstractmethod
    def has_child(self, identifier) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove_child(self, identifier: int) -> 'AbstractEntity':
        raise NotImplementedError

    @abstractmethod
    def destroy(self) -> None:
        raise NotImplementedError


_ET = TypeVar('_ET', bound="Entity")


class Entity(AbstractEntity):
    def __init__(
            self,
            *,
            app: Simpli,
            name: str | None = None,
            parent: AbstractEntity | None = None,
    ) -> None:
        super().__init__(app=app)

        self._name: str | None = name
        self._parent: AbstractEntity | None = parent
        self._children: AbstractIdentifierHolder = IdentifierHolder()
        self._components: AbstractComponentHolder = ComponentHolder(app=app, entity=self)

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def parent(self) -> AbstractEntity | None:
        return self._parent

    @property
    def children(self) -> Iterable[AbstractEntity]:
        return map(self.app.entities.__getitem__, self._children.__iter__())

    @property
    def components(self) -> AbstractComponentHolder:
        return self._components

    def _set_parent(self, parent: AbstractEntity | None) -> None:
        self._parent = parent

    def add_child(self, child_type: Type[_AET], *args: Any, **kwargs: Any) -> _AET:
        child: _AET = self.app.entities.new(child_type, *args, **kwargs)
        self._children.add(child.identifier)
        child._set_parent(self)
        return child

    def set_child(self, child: _AET) -> _AET:
        if child.identifier in self._children:
            raise ValueError(f"Entity {child.identifier} is already a child of {self.identifier}")

        if child.parent is not None:
            child.parent.remove_child(child.identifier)

        self._children.add(child.identifier)
        child._set_parent(self)
        return child

    def has_child(self, identifier) -> bool:
        return identifier in self._children

    def remove_child(self, identifier: int) -> AbstractEntity:
        if identifier not in self._children:
            raise KeyError(f"Entity {identifier} is not a child of {self.identifier}")

        self._children.remove(identifier)
        child: AbstractEntity = self.app.entities[identifier]
        child._set_parent(None)
        return child

    def destroy(self) -> None:
        self.app.entities.remove(self.identifier)
