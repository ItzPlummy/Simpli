from abc import ABC, abstractmethod
from typing import ClassVar, get_args, get_origin

from pyglet.graphics import Batch, Group
from pyglet.shapes import ShapeBase

from simpli.components.motion import PositionComponent
from simpli.components.shape import ShapeComponent
from simpli.renderers import Renderer
from simpli.spaces import Space
from simpli.systems import FrameSystem, TickSystem
from simpli.utils import Vector


class ShapeRenderSystem[T: ShapeComponent, O: ShapeBase](TickSystem, FrameSystem, ABC):
    shape_type: ClassVar[type[ShapeComponent]]

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        for base in cls.__dict__.get("__orig_bases__", ()):
            if get_origin(base) is ShapeRenderSystem:
                cls.shape_type = get_args(base)[0]

        if not hasattr(cls, "shape_type"):
            raise TypeError(f"Unable to determine shape type for {cls.__name__}")

    def __init__(self) -> None:
        self._bases: dict[int, O] = {}
        self._previous_positions: dict[int, Vector] = {}
        self._current_positions: dict[int, Vector] = {}

    @abstractmethod
    def create(
            self,
            shape: T,
            batch: Batch,
            group: Group,
    ) -> O:
        ...

    @abstractmethod
    def update(
            self,
            base: O,
            shape: T,
    ) -> None:
        ...

    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        renderer: Renderer = space.resources.get(Renderer)
        seen: set[int] = set()

        for entity in space.entities.by_components(PositionComponent, self.shape_type):
            seen.add(entity.id)

            position: PositionComponent = entity.get(PositionComponent)
            shape: T = entity.get(self.shape_type)
            target: Vector = position.position + shape.offset

            base: O | None = self._bases.get(entity.id)

            if base is None:
                base: O = self.create(shape, renderer.batch, renderer.layer(shape.layer))
                self._bases[entity.id] = base
                self._previous_positions[entity.id] = target
            else:
                self._previous_positions[entity.id] = self._current_positions[entity.id]

            self._current_positions[entity.id] = target

            self._apply_common(base, shape, renderer)
            self.update(base, shape)

        for entity_id in self._bases.keys() - seen:
            self._bases.pop(entity_id).delete()
            del self._previous_positions[entity_id], self._current_positions[entity_id]

    def on_frame(
            self,
            space: Space,
            alpha: int | float,
    ) -> None:
        for entity_id, base in self._bases.items():
            previous_position, current_position = self._previous_positions[entity_id], self._current_positions[entity_id]
            point: Vector = current_position if previous_position == current_position else previous_position + (current_position - previous_position) * alpha
            position: tuple[int | float, int | float] = point.x, point.y

            if base.position != position:
                base.position = position

    @staticmethod
    def _apply_common(
            base: O,
            shape: T,
            renderer: Renderer,
    ) -> None:
        rgba: tuple[int | float, ...] = tuple[int | float, ...](round(c * 255) for c in shape.color.as_tuple)

        if base.color != rgba:
            base.color = rgba

        if base.visible != shape.is_visible:
            base.visible = shape.is_visible

        group: Group = renderer.layer(shape.layer)

        if base.group is not group:
            base.group = group
