from simpli.components import Component
from simpli.utils import Vector, Resolvable


class VelocityComponent(Component):
    velocity: Resolvable[Vector] = Vector.zero()
