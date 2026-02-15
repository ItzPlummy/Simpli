from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, TypeVar, Iterable, Optional, Sequence, Tuple, Type, Dict

from simpli.components import AbstractComponentHolder, ComponentHolder
from simpli.components import Component
from simpli.interfaces import AppDependant, Identifiable
from simpli.utils import AbstractIdentifierHolder, IdentifierHolder

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

    def __init__(self, app: Simpli) -> None:
        self._app: Simpli = app
        self._identifier: int | None = None

    @property
    def app(self) -> Simpli:
        return self._app

    @property
    def identifier(self) -> int:
        if self._identifier is None:
            raise ValueError("Identifier is not set")

        return self._identifier

    def set_identifier_if_none(self, identifier: int) -> None:
        if identifier is None:
            raise ValueError("Identifier cannot be None")

        if self._identifier is not None:
            raise ValueError("Identifier is already set")

        self._identifier = identifier


_ET = TypeVar('_ET', bound="Entity")


class Entity(AbstractEntity):
    def __init__(
            self,
            *,
            app: Simpli,
            name: str | None = None,
            parent: AbstractEntity | None = None,
            components: Sequence[Tuple[Type[Component], Dict[str, Any]]] | None = None,
    ) -> None:
        super().__init__(app=app)

        self._name: str | None = name
        self._parent: AbstractEntity | None = parent
        self._children: AbstractIdentifierHolder = IdentifierHolder()
        self._components: AbstractComponentHolder = ComponentHolder(app=app, entity=self)

        if components:
            for component_type, kwargs in components:
                self._components.add(component_type, **kwargs)

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
