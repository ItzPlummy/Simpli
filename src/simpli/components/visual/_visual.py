from simpli.components import Component
from simpli.utils import Vector, Resolvable


class VisualComponent(Component):
    is_visible: Resolvable[bool] = True
    layer: Resolvable[int] = 0

    offset: Resolvable[Vector] = Vector.zero()
    direction: Resolvable[Vector] = Vector.zero()
