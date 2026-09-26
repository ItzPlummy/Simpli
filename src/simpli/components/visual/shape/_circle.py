from simpli.components.visual.shape._shape import ShapeComponent
from simpli.utils import Resolvable


class CircleComponent(ShapeComponent):
    radius: Resolvable[int | float]
