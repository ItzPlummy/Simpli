from abc import ABC, abstractmethod


class Tagged(ABC):
    @classmethod
    @abstractmethod
    def tag(cls) -> str:
        raise NotImplementedError
