from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from simpli.interfaces import AppDependant, EntityDependant, Tagged

if TYPE_CHECKING:
    from simpli import Simpli
    from simpli.entities import AbstractEntity
else:
    Simpli = Any
    AbstractEntity = Any


@dataclass(kw_only=True, slots=True)
class Component(AppDependant, EntityDependant, Tagged, ABC):
    _app: Simpli
    _entity: AbstractEntity

    @property
    def app(self) -> Simpli:
        return self._app

    @property
    def entity(self) -> AbstractEntity:
        return self._entity
