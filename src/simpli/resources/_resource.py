from abc import ABC, abstractmethod


class Resource(ABC):
    @classmethod
    @abstractmethod
    def tag(cls) -> str:
        ...
