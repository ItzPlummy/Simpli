from abc import abstractmethod, ABC
from array import array
from functools import partial
from typing import Generic, TypeVar, List, Iterable

_T = TypeVar('_T', bound=object)


class AbstractHolder(Generic[_T], ABC):
    @abstractmethod
    def add(self, item: _T) -> int:
        raise NotImplementedError

    @abstractmethod
    def remove(self, identifier: int) -> _T:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, identifier: int) -> _T:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, identifier: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable[_T]:
        raise NotImplementedError


class Holder(AbstractHolder, Generic[_T]):
    __slots__ = (
        "_items",
        "_ids",
        "_indices"
    )

    def __init__(self) -> None:
        self._items: List[_T] = []
        self._ids: array = array('I')
        self._indices: array = array('I')

        self._current_iterations: int = 0
        self._pending_operations: List[partial] = []

    def add(self, item: _T) -> int:
        self._items.append(item)
        index: int = len(self._items) - 1

        try:
            identifier: int = self._ids[index]
        except IndexError:
            self._ids.append(index)
            self._indices.append(index)
            identifier: int = index

        return identifier

    def remove(self, identifier: int) -> _T:
        try:
            index: int = self._indices[identifier]
        except IndexError:
            raise KeyError(f"Id {identifier} is not in holder")

        self._items[index], self._items[-1] = self._items[-1], self._items[index]
        self._ids[index], self._ids[-1] = self._ids[-1], self._ids[identifier]
        (
            self._indices[self._ids[index]],
            self._indices[self._ids[-1]]
        ) = (
            self._indices[self._ids[-1]],
            self._indices[self._ids[index]]
        )

        return self._items.pop()

    def __getitem__(self, identifier: int) -> _T:
        try:
            return self._items[self._indices[identifier]]
        except IndexError:
            raise KeyError(f"ID {identifier} is not in holder")

    def __contains__(self, identifier: int) -> bool:
        try:
            return self._indices[identifier] < len(self._items)
        except IndexError:
            return False

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterable[_T]:
        self._current_iterations += 1

        try:
            for item in self._items:
                yield item
        finally:
            self._current_iterations -= 1

            if self._current_iterations <= 0:
                self._current_iterations = 0
                self._flush_pending_operations()

    def _flush_pending_operations(self):
        for operation in self._pending_operations:
            operation()

        self._pending_operations.clear()
