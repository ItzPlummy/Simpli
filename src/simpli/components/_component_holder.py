from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING, Any, TypeVar, Type

from ._component import Component
from ..interfaces import AppDependant, EntityDependant

if TYPE_CHECKING:
    from simpli import Simpli
    from simpli.entities import AbstractEntity
else:
    Simpli = Any
    AbstractEntity = Any


_CT = TypeVar("_CT", bound=Component)


class AbstractComponentHolder(AppDependant, EntityDependant, ABC):
    @abstractmethod
    def add(self, component_type: Type[_CT], *args: Any, **kwargs: Any) -> _CT: ...

    @abstractmethod
    def get(self, component_type: Type[_CT]) -> _CT:
        raise NotImplementedError

    @abstractmethod
    def has(self, component_type: Type[_CT]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove(self, component_type: Type[_CT]) -> None:
        raise NotImplementedError

    def __init__(self, *, app: Simpli, entity: AbstractEntity) -> None:
        self._app: Simpli = app
        self._entity: AbstractEntity = entity

    @property
    def app(self) -> Simpli:
        return self._app

    @property
    def entity(self) -> AbstractEntity:
        return self._entity

    def has_any(self, *component_types: Type[_CT]) -> bool:
        return any(self.has(component_type) for component_type in component_types)

    def has_all(self, *component_types: Type[_CT]) -> bool:
        return all(self.has(component_type) for component_type in component_types)


class ComponentHolder(AbstractComponentHolder):
    def __init__(self, *, app: Simpli, entity: AbstractEntity) -> None:
        super().__init__(app=app, entity=entity)
        self._components: Dict[str, Component] = {}

    def add(self, component_type: Type[_CT], *args: Any, **kwargs: Any) -> _CT:
        component: _CT = component_type(_app=self.app, _entity=self.entity, *args, **kwargs)
        self._components[component_type.tag()] = component
        return component

    def get(self, component_type: Type[_CT]) -> _CT:
        try:
            return self._components[component_type.tag()]
        except KeyError:
            raise KeyError(f"Component \"{component_type.tag()}\" was not found")

    def has(self, component_type: Type[_CT]) -> bool:
        return component_type.tag() in self._components

    def remove(self, component_type: Type[_CT]) -> None:
        try:
            self._components.pop(component_type.tag())
        except KeyError:
            raise KeyError(f"Component \"{component_type.tag()}\" was not found")
