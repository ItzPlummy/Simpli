from typing import Iterable

from simpli.components import Component
from simpli.utils import Supplier


class ComponentCollection(Supplier[Iterable[Component]]):
    def __init__(self, *components: Component):
        super().__init__(lambda: components)
