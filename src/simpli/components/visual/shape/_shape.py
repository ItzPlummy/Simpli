from simpli.components.visual import VisualComponent
from simpli.utils import Color, Resolvable


class ShapeComponent(VisualComponent):
    color: Resolvable[Color]
