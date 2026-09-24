from simpli.counters._counter import Counter
from simpli.counters._time import Time
from simpli.spaces import Space
from simpli.utils import Resolvable, resolve


class DefaultCounter(Counter):
    def __init__(
            self,
            space: Space,
            tps: Resolvable[int | float] | None = None,
            fps: Resolvable[int | float] | None = None,
    ) -> None:
        self._space: Space = space

        self._tps: Resolvable[int | float] = tps or 60
        self._fps: Resolvable[int | float] = fps or 240
        self._time_scale: Resolvable[int | float] = 1.0
        self._is_paused: Resolvable[bool] = False

        self._time: Time = Time(0, 0, 1 / self.tps, 0)
        self._accumulator: int | float = 0

    @property
    def tps(self) -> int | float:
        return self._resolve_positive_float(self._tps)

    @tps.setter
    def tps(self, tps: Resolvable[int | float]) -> None:
        self._tps = tps if callable(tps) else self._resolve_positive_float(tps)

    @property
    def fps(self) -> int | float:
        return self._resolve_positive_float(self._fps)

    @fps.setter
    def fps(self, fps: Resolvable[int | float]) -> None:
        self._fps = fps if callable(fps) else self._resolve_positive_float(fps)

    @property
    def time_scale(self) -> Resolvable[int | float]:
        return self._resolve_positive_float(self._time_scale)

    @time_scale.setter
    def time_scale(self, time_scale: Resolvable[int | float]) -> None:
        self._time_scale = time_scale if callable(time_scale) else self._resolve_positive_float(time_scale)

    @property
    def is_paused(self) -> bool:
        return self._resolve_bool(self._is_paused)

    @is_paused.setter
    def is_paused(self, is_paused: Resolvable[bool]) -> None:
        self._is_paused = is_paused if callable(is_paused) else self._resolve_bool(is_paused)

    @property
    def time(self) -> Time:
        return self._time

    def advance(
            self,
            real_delta: int | float,
    ) -> int | float:
        if not self.is_paused:
            self._accumulator += min(real_delta, 1 / self.fps) * self.time_scale

        while self._accumulator >= self.time.delta:
            self._tick()
            self._accumulator -= self.time.delta

        self.time.alpha = self._accumulator / self.time.delta
        return self.time.alpha

    def step(self) -> None:
        self._tick()

    def _tick(self) -> None:
        self._space.step(self.time.delta)
        self.time.tick += 1
        self.time.simulation_time += self.time.delta

    @classmethod
    def _resolve_positive_float(
            cls,
            value: Resolvable[int | float]
    ) -> int | float:
        value: int | float = resolve(value)

        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a real number")

        if value <= 0:
            raise ValueError("Value must be a positive real number")

        return value

    @classmethod
    def _resolve_bool(
            cls,
            value: Resolvable[bool],
    ) -> bool:
        return bool(resolve(value))
