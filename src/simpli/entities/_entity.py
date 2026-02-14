from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING, Any, TypeVar, Iterable, Self

from simpli.components import Component
from simpli.components import AbstractComponentHolder, ComponentHolder
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
    def parent(self) -> Self | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def children(self) -> Iterable[Self]:
        raise NotImplementedError

    @property
    @abstractmethod
    def components(self) -> AbstractComponentHolder:
        raise NotImplementedError

    @abstractmethod
    def add_child(self, child_type: Type[_AET], *args: Any, **kwargs: Any) -> _AET:
        raise NotImplementedError

    @abstractmethod
    def set_child(self, child: _AET) -> _AET:
        raise NotImplementedError

    @abstractmethod
    def has_child(self, identifier) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove_child(self, identifier: int) -> Self:
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
            identifier: int | None = None,
            parent: _ET | None = None,
    ) -> None:
        super().__init__(app=app, identifier=identifier)

        self._parent: _ET | None = parent
        self._children: AbstractIdentifierHolder = IdentifierHolder()
        self._components: AbstractComponentHolder = ComponentHolder(app=app, entity=self)

    @property
    def parent(self) -> _ET | None:
        return self._parent

    def _set_parent(self, parent: _ET | None) -> None:
        self._parent = parent

    @property
    def children(self) -> Iterable[_ET]:
        return map(self.app.entities.__getitem__, self._children.__iter__())

    @property
    def components(self) -> AbstractComponentHolder:
        return self._components

    def add_child(self, child_type: Type[_ET], *args: Any, **kwargs: Any) -> _ET:
        child: _ET = self.app.entities.new(child_type, *args, **kwargs)
        self._children.add(child.identifier)
        child._set_parent(self)
        return child

    def set_child(self, child: _ET) -> _ET:
        if child.identifier in self._children:
            raise ValueError(f"Entity {child.identifier} is already a child of {self.identifier}")

        if child.parent is not None:
            child.parent.remove_child(child.identifier)

        self._children.add(child.identifier)
        child._set_parent(self)
        return child

    def has_child(self, identifier) -> bool:
        return identifier in self._children

    def remove_child(self, identifier: int) -> _ET:
        if identifier not in self._children:
            raise KeyError(f"Entity {identifier} is not a child of {self.identifier}")

        self._children.remove(identifier)
        child: _ET = self.app.entities[identifier]
        child._set_parent(None)
        return child

    def destroy(self) -> None:
        self.app.entities.remove(self.identifier)
