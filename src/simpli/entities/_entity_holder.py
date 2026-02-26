from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING, Any, Iterable, TypeVar, overload

from simpli.components import Component, PositionComponent
from simpli.entities import Entity, AbstractEntity
from simpli.interfaces import AppDependant, Archetype, ArchetypeID
from simpli.utils import Vector, ArchetypeHolder, AbstractArchetypeHolder

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
    def get(self, identifier: ArchetypeID[Component]) -> AbstractEntity:
        raise NotImplementedError

    @abstractmethod
    def has(self, identifier: ArchetypeID[Component]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove(self, identifier: ArchetypeID[Component]) -> None:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable[AbstractEntity]:
        raise NotImplementedError

    @abstractmethod
    def by_components(self, *component_types: Type[Component]) -> Iterable[AbstractEntity]:
        raise NotImplementedError

    @abstractmethod
    def nearby(self, position: Vector, radius: float, *component_types: Type[Component]) -> Iterable[AbstractEntity]:
        raise NotImplementedError

    def __init__(self, *, app: Simpli) -> None:
        self._app: Simpli = app

    @property
    def app(self) -> Simpli:
        return self._app


class EntityHolder(AbstractEntityHolder):
    def __init__(self, *, app: Simpli) -> None:
        super().__init__(app=app)
        self._entities: AbstractArchetypeHolder[Entity, Component] = ArchetypeHolder(app=app)

    def new(self, entity_type: Type[_ET] | None = None, *args: Any, **kwargs: Any) -> _ET:
        if entity_type is None:
            entity_type = Entity

        entity: _ET = entity_type(app=self.app, *args, **kwargs)
        self._entities.add(entity)

        return entity

    def get(self, identifier: ArchetypeID[Component]) -> Entity:
        return self._entities.get(identifier)

    def has(self, identifier: ArchetypeID[Component]) -> bool:
        return self._entities.has(identifier)

    def remove(self, identifier: ArchetypeID[Component]) -> Entity:
        entity: Entity = self.get(identifier)

        for child in entity.children:
            self.remove(child.archetype_id)

        if entity.parent is not None:
            entity.parent.remove_child(identifier)

        return self._entities.remove(identifier)

    def __len__(self) -> int:
        return len(self._entities)

    def __iter__(self) -> Iterable[Entity]:
        return self._entities.__iter__()

    def by_components(self, *component_types: Type[Component]) -> Iterable[Entity]:
        return self._entities.by_archetype(Archetype(*component_types))

    def nearby(self, position: Vector, radius: float, *component_types: Type[Component]) -> Iterable[Entity]:
        for entity in self.by_components(PositionComponent, *component_types):
            if (entity.get_component(PositionComponent).position - position).length < radius:
                yield entity
