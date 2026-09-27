from simpli.components import Component
from simpli.utils import Resolvable


class BouncyAppearanceEffectComponent(Component):
    start_tick: Resolvable[int]
    amplitude: Resolvable[int | float] = 0.25
    frequency: Resolvable[int | float] = 1.25
    duration: Resolvable[int | float] = 120
