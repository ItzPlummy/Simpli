from abc import ABC, abstractmethod


class Identifiable(ABC):
    @property
    @abstractmethod
    def identifier(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_identifier_if_none(self, identifier: int) -> None:
        raise NotImplementedError
