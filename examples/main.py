from simpli import Simpli, Vector, MouseButton, VelocityComponent, PositionComponent
from simpli.entities import CellEntity


class MyApp(Simpli):
    def on_mouse_click(
            self,
            position: Vector,
            button: MouseButton,
    ) -> None:
        if button == MouseButton.LEFT:
            for i in range(5):
                self.entities.new(CellEntity, position + Vector.random() * 50, 40)
        else:
            repulsion_radius: float = 500

            for entity in self.entities.nearby(position, repulsion_radius, PositionComponent, VelocityComponent):
                entity_position: Vector = entity.components.get(PositionComponent).position
                distance: Vector = entity_position - position
                entity.components.get(VelocityComponent).velocity += distance.normalized * (repulsion_radius - distance.length) * 0.05


MyApp().run()
