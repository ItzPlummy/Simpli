from simpli.components import Component
from simpli.utils import Resolvable


class RepulsionComponent(Component):
    max_repulsion: Resolvable[int | float]
    max_distance: Resolvable[int | float]
