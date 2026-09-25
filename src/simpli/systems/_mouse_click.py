from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from simpli.enums import MouseButton
from simpli.systems._system import System
from simpli.utils import Vector

if TYPE_CHECKING:
    from simpli.spaces import Space
else:
    Space = Any


class MouseClickSystem(System, ABC, is_kind=True):
    @abstractmethod
    def on_mouse_click(
            self,
            space: Space,
            position: Vector,
            screen_position: Vector,
            mouse_button: MouseButton,
    ) -> None:
        ...
