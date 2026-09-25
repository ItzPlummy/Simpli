from pyglet.graphics import Batch, Group
from pyglet.shapes import Circle

from simpli.components.shape import CircleComponent
from simpli.systems.render.shape._shape import ShapeRenderSystem


class CircleRenderSystem(ShapeRenderSystem[CircleComponent, Circle]):
    def create(
            self,
            shape: CircleComponent,
            batch: Batch,
            group: Group,
    ) -> Circle:
        return Circle(0, 0, shape.radius, batch=batch, group=group)

    def update(
            self,
            base: Circle,
            shape: CircleComponent,
    ) -> None:
        if base.radius != shape.radius:
            base.radius = shape.radius
