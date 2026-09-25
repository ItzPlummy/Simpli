from simpli.components import Component
from simpli.utils import Vector


class VisualComponent(Component):
    is_visible: bool = True
    layer: int = 0

    offset: Vector = Vector.zero()
    direction: Vector = Vector.zero()
