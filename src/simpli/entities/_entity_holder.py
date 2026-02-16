from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING, Any, Iterable, TypeVar, overload

from simpli.components import Component, PositionComponent
from simpli.entities import Entity, AbstractEntity
from simpli.interfaces import AppDependant
from simpli.utils import Holder, Vector

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any

_CT = TypeVar("_CT", bound=Component)
_AET = TypeVar("_AET", bound=AbstractEntity)
_ET = TypeVar("_ET", bound=Entity)


class AbstractEntityHolder(AppDependant, ABC):
    @overload
    def new(self, *args: Any, **kwargs: Any) -> AbstractEntity: ...

    @overload
    def new(self, entity_type: Type[_AET], *args: Any, **kwargs: Any) -> _AET: ...

    @abstractmethod
    def new(self, entity_type: Type[_AET] | None = None, *args: Any, **kwargs: Any) -> _AET:
        raise NotImplementedError

    @abstractmethod
    def remove(self, identifier: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, identifier: int) -> AbstractEntity:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, identifier: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable[AbstractEntity]:
        raise NotImplementedError

    @abstractmethod
    def by_components(self, *component_types: Type[_CT]) -> Iterable[AbstractEntity]:
        raise NotImplementedError

    @abstractmethod
    def nearby(self, position: Vector, radius: float, *component_types: Type[_CT]) -> Iterable[AbstractEntity]:
        raise NotImplementedError

    def __init__(self, *, app: Simpli) -> None:
        self._app: Simpli = app

    @property
    def app(self) -> Simpli:
        return self._app


class EntityHolder(AbstractEntityHolder):
    def __init__(self, *, app: Simpli) -> None:
        super().__init__(app=app)
        self._entities: Holder[Entity] = Holder[Entity]()

    def new(self, entity_type: Type[_ET] | None = None, *args: Any, **kwargs: Any) -> _ET:
        if entity_type is None:
            entity_type = Entity

        entity: _ET = entity_type(app=self.app, *args, **kwargs)
        self._entities.add(entity)

        return entity

    def remove(self, identifier: int) -> Entity:
        entity: Entity = self[identifier]

        for child in entity.children:
            self.remove(child.identifier)

        if entity.parent is not None:
            entity.parent.remove_child(entity.identifier)

        return self._entities.remove(identifier)

    def __getitem__(self, identifier: int) -> Entity:
        try:
            return self._entities[identifier]
        except KeyError:
            raise KeyError(f"Entity \"{identifier}\" is not in holder")

    def __contains__(self, identifier: int) -> bool:
        return identifier in self._entities

    def __len__(self) -> int:
        return len(self._entities)

    def __iter__(self) -> Iterable[Entity]:
        return self._entities.__iter__()

    def by_components(self, *component_types: Type[_CT]) -> Iterable[Entity]:
        for entity in self._entities:
            if entity.components.has_all(*component_types):
                yield entity

    def nearby(self, position: Vector, radius: float, *component_types: Type[_CT]) -> Iterable[Entity]:
        for entity in self.by_components(PositionComponent, *component_types):
            if (entity.components.get(PositionComponent).position - position).length < radius:
                yield entity
