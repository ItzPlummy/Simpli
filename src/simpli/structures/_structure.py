from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from simpli.entities import Entity

if TYPE_CHECKING:
    from simpli.spaces import Space
else:
    Space = Any


class Structure(ABC):
    @abstractmethod
    def place(
            self,
            space: Space,
    ) -> Entity:
        ...
