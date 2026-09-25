from simpli.components import Component
from simpli.utils import Vector, Resolvable


class PositionComponent(Component):
    position: Resolvable[Vector]
