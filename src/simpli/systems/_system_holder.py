from abc import abstractmethod, ABC
from collections import defaultdict
from typing import Type, TypeVar, Iterable, TYPE_CHECKING, Any, Dict

from simpli.systems import System
from simpli.utils import Holder, AppDependant

_TS = TypeVar('_TS', bound=System)

if TYPE_CHECKING:
    from simpli import Simpli
else:
    Simpli = Any


class AbstractSystemHolder(AppDependant, ABC):
    @abstractmethod
    def add(self, *systems: Type[_TS]) -> None:
        raise NotImplementedError

    @abstractmethod
    def by_system(self, system_type: Type[_TS]) -> Iterable[_TS]:
        raise NotImplementedError


class SystemHolder(AbstractSystemHolder):
    def __init__(self, app: Simpli, **kwargs: Any) -> None:
        super().__init__(app=app, **kwargs)
        self._app: Simpli = app
        self._systems: Dict[str, Holder[_TS]] = defaultdict(Holder)

    def add(self, *systems: Type[_TS]) -> None:
        for system in systems:
            self._add(system)

    def _add(self, system: Type[_TS]) -> None:
        self._systems[system.system_tag()].add(system(self._app))

    def by_system(self, system_type: Type[_TS]) -> Iterable[_TS]:
        return self._systems[system_type.system_tag()].__iter__()
