from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from simpli.systems._system import System

if TYPE_CHECKING:
    from simpli.spaces import Space
else:
    Space = Any


class StartSystem(System, ABC, is_kind=True):
    @abstractmethod
    def on_start(
            self,
            space: Space,
    ) -> None:
        ...
