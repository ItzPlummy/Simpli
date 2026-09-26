from simpli.components import Component
from simpli.utils import Resolvable


class AttractionComponent(Component):
    max_attraction: Resolvable[int | float]
    max_distance: Resolvable[int | float]
