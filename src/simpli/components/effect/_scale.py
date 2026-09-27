from simpli.components import Component
from simpli.utils import Resolvable


class ScaleEffectComponent(Component):
    scale: Resolvable[int | float] = 1
