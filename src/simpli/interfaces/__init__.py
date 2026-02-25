from abc import ABC

from simpli.interfaces._app_dependant import AppDependant
from simpli.interfaces._archetyped import Archetyped, Archetype
from simpli.interfaces._entity_dependant import EntityDependant
from simpli.interfaces._identifiable import Identifiable
from simpli.interfaces._tagged import Tagged


class ArchetypedIdentifiable(Archetyped, Identifiable, ABC):
    pass


__all__ = [
    AppDependant,
    Archetype,
    Archetyped,
    ArchetypedIdentifiable,
    EntityDependant,
    Identifiable,
    Tagged,
]
