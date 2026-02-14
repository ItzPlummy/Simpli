from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from simpli.utils import Tagged

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any


class System(Tagged, ABC):
    def __init__(self, app: Simpli) -> None:
        self._app: Simpli = app

    @property
    def app(self) -> Simpli:
        return self._app

    @classmethod
    @abstractmethod
    def system_tag(cls) -> str:
        raise NotImplementedError


class TickSystem(System, ABC):
    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError

    @classmethod
    def system_tag(cls) -> str:
        return "tick"
