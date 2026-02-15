from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any


class AppDependant(ABC):
    @property
    @abstractmethod
    def app(self) -> Simpli:
        raise NotImplementedError
