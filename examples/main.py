from random import random

from simpli import Simpli, Vector, MouseButton, Color
from simpli.entities import RepulsiveCircleEntity


class MyApp(Simpli):
    def on_mouse_click(
            self,
            position: Vector,
            button: MouseButton,
    ) -> None:
        self.entities.new(RepulsiveCircleEntity, position + Vector(-640, -360), random() * 100 + 10, Color.random_dark())


MyApp().run()
