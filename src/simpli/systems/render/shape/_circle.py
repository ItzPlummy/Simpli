from pyglet.graphics import Batch, Group
from pyglet.shapes import Circle

from simpli.components.visual.shape import CircleComponent
from simpli.systems.render.shape._shape import ShapeRenderSystem
from simpli.utils import resolve


class CircleRenderSystem(ShapeRenderSystem[CircleComponent, Circle]):
    def create(
            self,
            shape: CircleComponent,
            scale: int | float,
            batch: Batch,
            group: Group,
    ) -> Circle:
        return Circle(
            0,
            0,
            resolve(shape.radius) * scale,
            batch=batch,
            group=group,
        )

    def update(
            self,
            base: Circle,
            shape: CircleComponent,
    ) -> None:
        pass

    def apply_scale(
            self,
            base: Circle,
            shape: CircleComponent,
            scale: int | float,
    ) -> None:
        radius: int | float = resolve(shape.radius) * scale

        if base.radius != radius:
            base.radius = radius
