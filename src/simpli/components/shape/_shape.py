from simpli.components import Component
from simpli.utils import Vector, Color


class ShapeComponent(Component):
    color: Color
    layer: int = 0
    is_visible: bool = True

    offset: Vector = Vector.zero()
