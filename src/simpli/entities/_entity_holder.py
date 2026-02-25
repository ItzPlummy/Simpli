from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING, Any, Iterable, TypeVar, overload

from simpli.components import Component, PositionComponent
from simpli.entities import Entity, AbstractEntity
from simpli.interfaces import AppDependant, Archetype
from simpli.utils import Vector, ArchetypeHolder

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
    def get(self, archetype: Archetype[Component], identifier: int) -> AbstractEntity:
        raise NotImplementedError

    @abstractmethod
    def has(self, archetype: Archetype[Component], identifier: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove(self, archetype: Archetype[Component], identifier: int) -> None:
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
        self._entities: ArchetypeHolder[Component] = ArchetypeHolder[Component](app=app)

    def new(self, entity_type: Type[_ET] | None = None, *args: Any, **kwargs: Any) -> _ET:
        if entity_type is None:
            entity_type = Entity

        entity: _ET = entity_type(app=self.app, *args, **kwargs)
        self._entities.add(entity)

        return entity

    def remove(self, archetype: Archetype[Component], identifier: int) -> Entity:
        entity: Entity = self.get(archetype, identifier)

        for child in entity.children:
            self.remove(child.archetype, child.identifier)

        if entity.parent is not None:
            entity.parent.remove_child(entity.archetype, entity.identifier)

        return self._entities.remove(archetype, identifier)

    def get(self, archetype: Archetype[Component], identifier: int) -> Entity:
        return self._entities.get(archetype, identifier)

    def has(self, archetype: Archetype[Component], identifier: int) -> bool:
        return self._entities.has(archetype, identifier)

    def __len__(self) -> int:
        return len(self._entities)

    def __iter__(self) -> Iterable[Entity]:
        return self._entities.__iter__()

    def by_components(self, *component_types: Type[_CT]) -> Iterable[Entity]:
        return self._entities.by_archetype(Archetype(*component_types))

    def nearby(self, position: Vector, radius: float, *component_types: Type[_CT]) -> Iterable[Entity]:
        for entity in self.by_components(PositionComponent, *component_types):
            if (entity.get_component(PositionComponent).position - position).length < radius:
                yield entity
