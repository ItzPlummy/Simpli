from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING, TypeAlias, Callable, TypeVar

from simpli.interfaces import AppDependant, Identifiable
from simpli.enums import LayerGroup

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any

_T = TypeVar('_T', bound=object)
_EntityAttributeGetter: TypeAlias = Callable[[], _T]


@dataclass(kw_only=True, slots=True)
class Shape(AppDependant, Identifiable, ABC):
    _app: Simpli
    _identifier: int | None = None

    layer_group_getter: _EntityAttributeGetter[LayerGroup]
    layer_group: LayerGroup = LayerGroup.GEOMETRY

    @abstractmethod
    def create(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self) -> None:
        raise NotImplementedError

    @property
    def app(self) -> Simpli:
        return self._app

    @property
    def identifier(self) -> int:
        if self._identifier is None:
            raise ValueError("Identifier is not set")

        return self._identifier

    def set_identifier_if_none(self, identifier: int) -> None:
        if identifier is None:
            raise ValueError("Identifier cannot be None")

        if self._identifier is not None:
            raise ValueError("Identifier is already set")

        self._identifier = identifier
