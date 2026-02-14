from typing import Any

from simpli import Simpli, PositionComponent, VelocityComponent, AirFrictionComponent, Entity, ShapeComponent, Circle, \
    Color
from simpli.components import GravityComponent


class MyApp(Simpli):
    def __init__(self, **window_kwargs: Any):
        super().__init__(**window_kwargs)

        self.e = self.entities.new()
        self.e.components.add(PositionComponent)
        self.e.components.add(VelocityComponent)
        self.e.components.add(AirFrictionComponent)
        self.e.components.add(GravityComponent)
        self.e.add_child(Entity).components.add(
            ShapeComponent,
            Circle,
            position_getter=lambda e: e.parent.components.get(PositionComponent).position,
            radius_getter=lambda e: 10,
            color_getter=lambda e: Color(0, 0, 0)
        )


MyApp().run()
