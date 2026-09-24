from abc import ABC, abstractmethod


class System(ABC):
    @classmethod
    @abstractmethod
    def tag(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def kind(cls) -> str:
        ...
