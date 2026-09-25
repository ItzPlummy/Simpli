from itertools import chain
from typing import Iterable

from pyglet import app
from pyglet.clock import unschedule, schedule_interval
from pyglet.window import Window

from simpli.apps import App
from simpli.counters import DefaultCounter, Counter
from simpli.renderers import Renderer, DefaultRenderer
from simpli.spaces import Space, DefaultSpace
from simpli.systems import System
from simpli.systems.motion import VelocitySystem
from simpli.systems.render.shape import CircleRenderSystem
from simpli.utils import Resolvable, Color


class Simpli(App):
    _DEFAULT_SYSTEMS: Iterable[System] = [
        VelocitySystem(),
        CircleRenderSystem(),
    ]

    SYSTEMS: Iterable[System] = []

    def __init__(
            self,
            *,
            title: str | None = None,
            width: int | None = None,
            height: int | None = None,
            tps: Resolvable[int | float] | None = None,
            fps: Resolvable[int | float] | None = None,
    ) -> None:
        self._title: str = title or "Simpli"
        self._window = Window(width or 1280, height or 720, self._title, resizable=True, vsync=True)

        self._space: Space = DefaultSpace()
        self._renderer: Renderer = DefaultRenderer(Color.oat())
        self._counter: Counter = DefaultCounter(self.space, tps, fps)

        self.space.resources.add(self.renderer)

        self.window.push_handlers(on_draw=self._on_draw)

    @property
    def title(self) -> str:
        return self._title

    @property
    def space(self) -> Space:
        return self._space

    @property
    def renderer(self) -> Renderer:
        return self._renderer

    @property
    def counter(self) -> Counter:
        return self._counter

    @property
    def window(self) -> Window:
        return self._window

    def start(self) -> None:
        for system in chain(self._DEFAULT_SYSTEMS, self.SYSTEMS):
            self.space.systems.add(system)

        self.space.on_start()
        self._schedule()

        try:
            app.run(None)
        finally:
            unschedule(self._frame)

    def stop(self) -> None:
        app.exit()

    def _schedule(self) -> None:
        unschedule(self._frame)
        schedule_interval(self._frame, 1 / self.counter.fps)

    def _frame(self, delta: int | float) -> None:
        if self.window.has_exit:
            unschedule(self._frame)
            return

        alpha = self.counter.advance(delta)
        self.space.on_frame(alpha)
        self.window.draw(delta)

    def _on_draw(self) -> None:
        self.renderer.draw(self.window)
