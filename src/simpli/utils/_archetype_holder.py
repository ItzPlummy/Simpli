from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, TypeVar, Generic, Iterable, TYPE_CHECKING, Any

from ._holder import Holder

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any

from simpli.interfaces import Tagged, ArchetypedIdentifiable, Archetype, ArchetypeID

_T = TypeVar("_T", bound=Tagged)
_AIT = TypeVar("_AIT", bound=ArchetypedIdentifiable)


class AbstractArchetypeHolder(Generic[_AIT, _T], ABC):
    @abstractmethod
    def add(self, item: ArchetypedIdentifiable[_T]) -> ArchetypeID[_T]:
        raise NotImplementedError

    @abstractmethod
    def get(self, identifier: ArchetypeID[_T]) -> ArchetypedIdentifiable[_T]:
        raise NotImplementedError

    @abstractmethod
    def has(self, identifier: ArchetypeID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove(self, identifier: ArchetypeID[_T]) -> ArchetypedIdentifiable[_T]:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable[ArchetypedIdentifiable]:
        raise NotImplementedError

    @abstractmethod
    def by_archetype(self, archetype: Archetype[_T]) -> Iterable[ArchetypedIdentifiable[_T]]:
        raise NotImplementedError

    def __init__(self, *, app: Simpli) -> None:
        self._app: Simpli = app

    @property
    def app(self) -> Simpli:
        return self._app


class ArchetypeHolder(AbstractArchetypeHolder[_AIT, _T]):
    def __init__(self, *, app: Simpli) -> None:
        super().__init__(app=app)
        self._holders: Dict[Archetype[_T], Holder[ArchetypedIdentifiable[_T]]] = defaultdict(Holder)

    def add(self, item: ArchetypedIdentifiable[_T]) -> ArchetypeID[_T]:
        identifier: int = self._holders[item.archetype].add(item)
        item.set_identifier_if_none(identifier)
        return ArchetypeID(item.archetype, identifier)

    def get(self, identifier: ArchetypeID[_T]) -> ArchetypedIdentifiable[_T]:
        return self._holders[identifier.archetype][identifier.identifier]

    def has(self, identifier: ArchetypeID) -> bool:
        return identifier.identifier in self._holders[identifier.archetype]

    def remove(self, identifier: ArchetypeID[_T]) -> ArchetypedIdentifiable[_T]:
        return self._holders[identifier.archetype].remove(identifier.identifier)

    def __len__(self) -> int:
        return sum(map(len, self._holders.values()))

    def __iter__(self) -> Iterable[ArchetypedIdentifiable]:
        for holder in self._holders.values():
            for item in holder:
                yield item

    def by_archetype(self, archetype: Archetype[_T]) -> Iterable[ArchetypedIdentifiable[_T]]:
        for holder_archetype, holder in self._holders.items():
            if archetype <= holder_archetype:
                for item in holder:
                    yield item
