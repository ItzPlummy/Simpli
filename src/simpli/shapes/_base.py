from abc import ABC, abstractmethod
from typing import Any

from simpli.utils import Identifiable, AppDependant, EntityDependant


class Shape(AppDependant, EntityDependant, Identifiable, ABC):
    @abstractmethod
    def create(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self) -> None:
        raise NotImplementedError
