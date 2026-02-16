from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from simpli.interfaces import AppDependant
from simpli.utils import Vector

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any


class AbstractCamera(AppDependant, ABC):
    @property
    @abstractmethod
    def position(self) -> Vector:
        raise NotImplementedError

    @property
    @abstractmethod
    def target_position(self) -> Vector:
        raise NotImplementedError

    @target_position.setter
    @abstractmethod
    def target_position(self, value: Vector) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def zoom(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def target_zoom(self) -> float:
        raise NotImplementedError

    @target_zoom.setter
    @abstractmethod
    def target_zoom(self, value: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def adjust_zoom_by_scroll(self, scroll: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def position_from_window(self, window_position: Vector) -> Vector:
        raise NotImplementedError

    @abstractmethod
    def target_position_from_window(self, window_position: Vector) -> Vector:
        raise NotImplementedError

    @abstractmethod
    def captures_radius(self, position: Vector, radius: float) -> bool:
        raise NotImplementedError

    def __init__(self, *, app: Simpli) -> None:
        self._app: Simpli = app

    @property
    def app(self) -> Simpli:
        return self._app


class Camera(AbstractCamera):
    def __init__(
            self,
            *,
            app: Simpli,
            zoom_exponential_factor: float = 1.25,
            smoothness: float = 0.2,
            min_zoom: float = 0.2,
            max_zoom: float = 5.0,
            area_width: float = 12800,
            area_height: float = 7200,
    ) -> None:
        super().__init__(app=app)

        self._zoom_exponential_factor: float = zoom_exponential_factor
        self._smoothness: float = smoothness
        self._min_zoom: float = min_zoom
        self._max_zoom: float = max_zoom
        self._area_width: float = area_width
        self._area_height: float = area_height

        self._position: Vector = Vector.zero()
        self._target_position: Vector = Vector.zero()
        self._zoom: float = 1
        self._target_zoom: float = 1

    @property
    def position(self) -> Vector:
        return self._position

    @property
    def target_position(self) -> Vector:
        return self._target_position

    @target_position.setter
    def target_position(self, value: Vector) -> None:
        x, y = value.as_tuple

        if abs(x) > self.max_x_position:
            x = self.max_x_position * x / abs(x)
        if abs(y) > self.max_y_position:
            y = self.max_y_position * y / abs(y)

        self._target_position = Vector(x, y)

    @property
    def zoom(self) -> float:
        return self._zoom

    @property
    def target_zoom(self) -> float:
        return self._target_zoom

    @target_zoom.setter
    def target_zoom(self, value: float) -> None:
        self._target_zoom = min(max(value, self._min_zoom), self._max_zoom)

    @property
    def max_x_position(self) -> float:
        return (self._area_width - self.app.window_width / self.target_zoom) / 2

    @property
    def max_y_position(self) -> float:
        return (self._area_height - self.app.window_height / self.target_zoom) / 2

    def tick(self) -> None:
        if self._zoom != self._target_zoom:
            if abs(self._zoom - self._target_zoom) < 0.001:
                self._zoom = self._target_zoom
            else:
                self._zoom += (self._target_zoom - self._zoom) * self._smoothness

        if self._position != self._target_position:
            if (self._position - self._target_position).length_squared < 0.00001:
                self._position = self._target_position
            else:
                self._position += (self._target_position - self._position) * self._smoothness

    def adjust_zoom_by_scroll(self, scroll: float) -> None:
        zoom_factor: float = self._zoom_exponential_factor ** scroll

        mouse_position_before_zoom: Vector = self.app.mouse_position
        self.target_zoom *= zoom_factor
        mouse_position_after_zoom: Vector = self.app.mouse_position

        self.target_position += (mouse_position_before_zoom - mouse_position_after_zoom)

    def position_from_window(self, window_position: Vector) -> Vector:
        return (
                (window_position - Vector(self.app.window.width / 2, self.app.window.height / 2))
                * (1 / self._zoom) + self._position
        )

    def target_position_from_window(self, window_position: Vector) -> Vector:
        return (
                (window_position - Vector(self.app.window.width / 2, self.app.window.height / 2))
                * (1 / self._target_zoom) + self._target_position
        )

    def captures_radius(self, position: Vector, radius: float) -> bool:
        relative_position: Vector = position - self.position

        return (
                abs(relative_position.x) - radius < (self.app.window_width / self.zoom) / 2
                and abs(relative_position.y) - radius < (self.app.window_height / self.zoom) / 2
        )
