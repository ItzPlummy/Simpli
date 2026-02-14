from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from simpli.utils import Tagged, AppDependant, EntityDependant

if TYPE_CHECKING:
    from simpli import Simpli
    from simpli.entities import AbstractEntity
else:
    Simpli = Any
    AbstractEntity = Any


class Component(AppDependant, EntityDependant, Tagged, ABC):
    model_config = {
        "arbitrary_types_allowed": True,
        "slots": True,
    }

    @abstractmethod
    def __component_init__(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def __init__(self, *args: Any, app: Simpli, entity: AbstractEntity, **kwargs: Any):
        super().__init__(app=app, entity=entity)
        self.__component_init__(*args, **kwargs)
