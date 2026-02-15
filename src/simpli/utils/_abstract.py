from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from simpli import Simpli
    from simpli.entities import AbstractEntity
else:
    Simpli = Any
    AbstractEntity = Any


class AppDependant(ABC):
    def __init__(self, *, app: Simpli, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._app = app

    @property
    def app(self) -> Simpli:
        return self._app


class EntityDependant(ABC):
    def __init__(self, *, entity: AbstractEntity, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._entity = entity

    @property
    def entity(self) -> AbstractEntity:
        return self._entity


class Identifiable(ABC):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._identifier: int | None = None

    @property
    def identifier(self) -> int:
        if self._identifier is None:
            raise ValueError("Object has no identifier")

        return self._identifier

    @identifier.setter
    def identifier(self, value: int) -> None:
        if self._identifier is not None:
            raise ValueError("Object already has an identifier")

        self._identifier = value


class Tagged(ABC):
    @classmethod
    @abstractmethod
    def tag(cls) -> str:
        raise NotImplementedError
