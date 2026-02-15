from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from simpli.entities import AbstractEntity
else:
    AbstractEntity = Any


class EntityDependant(ABC):
    @abstractmethod
    def entity(self) -> AbstractEntity:
        raise NotImplementedError
