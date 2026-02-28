from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, TypeVar, Iterable, Optional, Sequence, Tuple, Type, Dict, Set

from simpli.components import Component
from simpli.interfaces import AppDependant, ArchetypedIdentifiable, ArchetypeID
from simpli.interfaces import Archetype

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any

_CT = TypeVar("_CT", bound=Component)
_AET = TypeVar("_AET", bound="AbstractEntity")


class AbstractEntity(AppDependant, ArchetypedIdentifiable[Component], ABC):
    @property
    @abstractmethod
    def name(self) -> str | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def parent(self) -> Optional['AbstractEntity']:
        raise NotImplementedError

    @property
    @abstractmethod
    def children(self) -> Iterable['AbstractEntity']:
        raise NotImplementedError

    @abstractmethod
    def _set_parent(self, parent: Optional['AbstractEntity']) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_child(self, child: _AET) -> _AET:
        raise NotImplementedError

    @abstractmethod
    def has_child(self, identifier: ArchetypeID[Component]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove_child(self, identifier: ArchetypeID[Component]) -> 'AbstractEntity':
        raise NotImplementedError

    @abstractmethod
    def add_component(self, component_type: Type[_CT], **kwargs: Any) -> _CT:
        raise NotImplementedError

    @abstractmethod
    def get_component(self, component_type: Type[_CT]) -> _CT:
        raise NotImplementedError

    @abstractmethod
    def has_component(self, component_type: Type[Component]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove_component(self, component_type: Type[Component]) -> None:
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

    def has_any_components(self, *component_types: Type[_CT]) -> bool:
        return any(self.has_component(component_type) for component_type in component_types)

    def has_all_components(self, *component_types: Type[_CT]) -> bool:
        return all(self.has_component(component_type) for component_type in component_types)


_ET = TypeVar('_ET', bound="Entity")


class Entity(AbstractEntity):
    def __init__(
            self,
            *,
            app: Simpli,
            name: str | None = None,
            parent: AbstractEntity | None = None,
            components: Sequence[Tuple[Type[_CT], Dict[str, Any]]] | None = None,
    ) -> None:
        super().__init__(app=app)

        self._name: str | None = name
        self._parent: AbstractEntity | None = parent
        self._children: Set[ArchetypeID[Component]] = set()
        self._components: Dict[str, _CT] = {}

        if components:
            for component_type, kwargs in components:
                self._components[component_type.tag()] = component_type(_app=app, _entity=self, **kwargs)

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def parent(self) -> AbstractEntity | None:
        return self._parent

    @property
    def children(self) -> Iterable[AbstractEntity]:
        return (self.app.entities.get(child_id) for child_id in self._children)

    @property
    def archetype(self) -> Archetype[_CT]:
        return Archetype(*self._components.values())

    def set_child(self, child: _AET) -> _AET:
        if child.archetype_id in self._children:
            raise ValueError(f"Entity {child.identifier} is already a child of {self.identifier}")

        if child.parent is not None:
            child.parent.remove_child(child.archetype_id)

        self._children.add(child.archetype_id)
        child._set_parent(self)
        return child

    def has_child(self, identifier: ArchetypeID[Component]) -> bool:
        return identifier in self._children

    def remove_child(self, identifier: ArchetypeID[Component]) -> AbstractEntity:
        if identifier not in self._children:
            raise KeyError(f"Entity {identifier} is not a child of {self.identifier}")

        self._children.remove(identifier)
        child: AbstractEntity = self.app.entities.get(identifier)
        child._set_parent(None)
        return child

    def add_component(self, component_type: Type[_CT], **kwargs: Any) -> _CT:
        component: _CT = component_type(_app=self.app, _entity=self, **kwargs)
        self._components[component_type.tag()] = component

        return component

    def get_component(self, component_type: Type[_CT]) -> _CT:
        try:
            return self._components[component_type.tag()]
        except KeyError:
            raise KeyError(f"Component \"{component_type.tag()}\" was not found")

    def has_component(self, component_type: Type[Component]) -> bool:
        return component_type.tag() in self._components

    def remove_component(self, component_type: Type[Component]) -> None:
        try:
            self._components.pop(component_type.tag())
        except KeyError:
            raise KeyError(f"Component \"{component_type.tag()}\" was not found")

    def destroy(self) -> None:
        self.app.entities.remove(self.archetype_id)

    def _set_parent(self, parent: AbstractEntity | None) -> None:
        self._parent = parent
