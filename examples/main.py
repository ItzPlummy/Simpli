from simpli import Simpli, Vector, MouseButton, VelocityComponent, PositionComponent
from simpli.entities import RepulsiveCircleEntity


class MyApp(Simpli):
    def on_mouse_click(
            self,
            position: Vector,
            button: MouseButton,
    ) -> None:
        if button == MouseButton.LEFT:
            self.entities.new(RepulsiveCircleEntity, position)
        else:
            repulsion_radius: float = 500

            for entity in self.entities.nearby(position, repulsion_radius, PositionComponent, VelocityComponent):
                entity_position: Vector = entity.components.get(PositionComponent).position
                distance: Vector = entity_position - position
                entity.components.get(VelocityComponent).velocity += distance.normalized * (repulsion_radius - distance.length) * 0.1


MyApp().run()
