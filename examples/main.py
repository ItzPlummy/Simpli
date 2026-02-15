from typing import Any

from simpli import Simpli, Vector, Color, VelocityComponent
from simpli.components import GravityComponent, AirFrictionComponent
from simpli.entities import CircleEntity


class MyApp(Simpli):
    def __init__(self, **window_kwargs: Any):
        super().__init__(**window_kwargs)

        a = self.entities.new(CircleEntity, Vector(100, 0), 10, Color.random_bright())
        a.components.add(VelocityComponent, velocity=Vector(-10, 0))
        a.components.add(AirFrictionComponent)
        a.components.add(GravityComponent)


MyApp().run()
