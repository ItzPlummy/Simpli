from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable

from simpli.interfaces import Identifiable
from simpli.utils import Holder

_IT = TypeVar('_IT', bound=Identifiable)


class AbstractIdentifiableHolder(Generic[_IT], ABC):
    @abstractmethod
    def add(self, item: _IT) -> int:
        raise NotImplementedError

    @abstractmethod
    def remove(self, identifier: int) -> _IT:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, identifier: int) -> _IT:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, identifier: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable[_IT]:
        raise NotImplementedError


class IdentifiableHolder(AbstractIdentifiableHolder, Generic[_IT]):
    def __init__(self) -> None:
        self._items: Holder[_IT] = Holder()

    def add(self, item: _IT) -> int:
        identifier: int = self._items.add(item)
        item.set_identifier_if_none(identifier)
        return identifier

    def remove(self, identifier: int) -> _IT:
        return self._items.remove(identifier)

    def __getitem__(self, identifier: int) -> _IT:
        return self._items[identifier]

    def __contains__(self, identifier: int) -> bool:
        return identifier in self._items

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterable[_IT]:
        return self._items.__iter__()
