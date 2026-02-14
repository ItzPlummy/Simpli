from abc import ABC, abstractmethod
from typing import Set, Iterable


class AbstractIdentifierHolder(ABC):
    @abstractmethod
    def add(self, identifier: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def remove(self, identifier: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, identifier: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable[int]:
        raise NotImplementedError

    def has_any(self, *identifiers: int) -> bool:
        return any(identifier in self for identifier in identifiers)

    def has_all(self, *identifiers: int) -> bool:
        return all(identifier in self for identifier in identifiers)


class IdentifierHolder(AbstractIdentifierHolder):
    def __init__(self) -> None:
        self._identifiers: Set[int] = set()

    def add(self, identifier: int) -> int:
        self._identifiers.add(identifier)
        return identifier

    def remove(self, identifier: int) -> int:
        self._identifiers.remove(identifier)
        return identifier

    def __contains__(self, identifier: int) -> bool:
        return identifier in self._identifiers

    def __len__(self) -> int:
        return len(self._identifiers)

    def __iter__(self) -> Iterable[int]:
        return self._identifiers.__iter__()
