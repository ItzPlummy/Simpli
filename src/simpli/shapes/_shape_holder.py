from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING, Any, Iterable, TypeVar

from simpli.interfaces import AppDependant
from simpli.shapes import Shape
from simpli.utils import Holder

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any
    AbstractEntity = Any

_ST = TypeVar("_ST", bound=Shape)


class AbstractShapeHolder(AppDependant, ABC):
    @abstractmethod
    def new(self, shape_type: Type[_ST], **kwargs: Any) -> _ST:
        raise NotImplementedError

    @abstractmethod
    def remove(self, identifier: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, identifier: int) -> Shape:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, identifier: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable[Shape]:
        raise NotImplementedError

    def __init__(self, *, app: Simpli) -> None:
        self._app: Simpli = app

    @property
    def app(self) -> Simpli:
        return self._app


class ShapeHolder(AbstractShapeHolder):
    def __init__(self, *, app: Simpli) -> None:
        super().__init__(app=app)
        self._shapes: Holder[Shape] = Holder()

    def new(self, shape_type: Type[_ST], **kwargs: Any) -> _ST:
        shape: _ST = shape_type(_app=self.app, **kwargs)
        self._shapes.add(shape)
        return shape

    def remove(self, identifier: int) -> Shape:
        return self._shapes.remove(identifier)

    def __getitem__(self, identifier: int) -> Shape:
        try:
            return self._shapes[identifier]
        except KeyError:
            raise KeyError(f"Shape \"{identifier}\" is not in holder")

    def __contains__(self, identifier: int) -> bool:
        return identifier in self._shapes

    def __len__(self) -> int:
        return len(self._shapes)

    def __iter__(self) -> Iterable[Shape]:
        return self._shapes.__iter__()
