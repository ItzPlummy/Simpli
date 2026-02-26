from abc import ABC
from dataclasses import dataclass
from typing import Self, Generic, TypeVar

from simpli.interfaces._app_dependant import AppDependant
from simpli.interfaces._archetyped import Archetyped, Archetype
from simpli.interfaces._entity_dependant import EntityDependant
from simpli.interfaces._identifiable import Identifiable
from simpli.interfaces._tagged import Tagged

_T = TypeVar("_T", bound=Tagged)


@dataclass(slots=True)
class ArchetypeID(Generic[_T]):
    archetype: Archetype[_T]
    identifier: int

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, ArchetypeID):
            return False
        return self.archetype == other.archetype and self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash((self.archetype, self.identifier))


class ArchetypedIdentifiable(Archetyped[_T], Identifiable, ABC):
    @property
    def archetype_id(self) -> ArchetypeID[_T]:
        return ArchetypeID(self.archetype, self.identifier)


__all__ = [
    AppDependant,
    Archetype,
    Archetyped,
    ArchetypedIdentifiable,
    EntityDependant,
    Identifiable,
    Tagged,
]
