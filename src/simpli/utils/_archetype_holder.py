from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, TypeVar, Generic, Iterable, TYPE_CHECKING, Any

from ._holder import Holder

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any

from simpli.interfaces import Tagged, ArchetypedIdentifiable, Archetype

_T = TypeVar("_T", bound=Tagged)
_AIT = TypeVar("_AIT", bound=ArchetypedIdentifiable)


class AbstractArchetypeHolder(Generic[_T, _AIT], ABC):
    @abstractmethod
    def add(self, item: _AIT) -> int:
        raise NotImplementedError

    @abstractmethod
    def get(self, archetype: Archetype[_T], identifier: int) -> _AIT:
        raise NotImplementedError

    @abstractmethod
    def has(self, archetype: Archetype[_T], identifier: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove(self, archetype: Archetype[_T], identifier: int) -> _AIT:
        raise NotImplementedError

    @abstractmethod
    def change_archetype(
            self,
            previous_archetype: Archetype[_T],
            new_archetype: Archetype[_T],
            identifier: int,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable[_AIT]:
        raise NotImplementedError

    @abstractmethod
    def by_archetype(self, archetype: Archetype[_T]) -> Iterable[_AIT]:
        raise NotImplementedError

    def __init__(self, *, app: Simpli) -> None:
        self._app: Simpli = app

    @property
    def app(self) -> Simpli:
        return self._app


class ArchetypeHolder(AbstractArchetypeHolder, Generic[_T]):
    def __init__(self, *, app: Simpli) -> None:
        super().__init__(app=app)
        self._holders: Dict[Archetype[_T], Holder[_AIT]] = defaultdict(Holder)

    def add(self, item: _AIT) -> int:
        identifier: int = self._holders[item.archetype].add(item)
        item.set_identifier_if_none(identifier)
        item.set_on_archetype_change_if_none(self.change_archetype)
        return identifier

    def get(self, archetype: Archetype[_T], identifier: int) -> _AIT:
        return self._holders[archetype][identifier]

    def has(self, archetype: Archetype[_T], identifier: int) -> bool:
        return identifier in self._holders[archetype]

    def remove(self, archetype: Archetype[_T], identifier: int) -> _AIT:
        return self._holders[archetype].remove(identifier)

    def change_archetype(
            self,
            identifier: int,
            previous_archetype: Archetype[_T],
            new_archetype: Archetype[_T],
    ) -> int:
        item: _AIT = self._holders[previous_archetype][identifier]
        self._holders[previous_archetype].remove(identifier)
        return self._holders[new_archetype].add(item)

    def __len__(self) -> int:
        return sum(map(len, self._holders.values()))

    def __iter__(self) -> Iterable[_AIT]:
        for holder in self._holders.values():
            for item in holder:
                yield item

    def by_archetype(self, archetype: Archetype[_T]) -> Iterable[_AIT]:
        for holder_archetype, holder in self._holders.items():
            if archetype <= holder_archetype:
                for item in holder:
                    yield item
