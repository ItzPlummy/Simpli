from abc import abstractmethod, ABC
from collections import defaultdict
from typing import Type, TypeVar, Iterable, TYPE_CHECKING, Any, Dict

from simpli.interfaces import AppDependant
from simpli.systems import System
from simpli.utils import Holder

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

    def __init__(self, *, app: Simpli) -> None:
        self._app: Simpli = app

    @property
    def app(self) -> Simpli:
        return self._app


class SystemHolder(AbstractSystemHolder):
    def __init__(self, *, app: Simpli) -> None:
        super().__init__(app=app)
        self._systems: Dict[str, Holder[_TS]] = defaultdict(Holder)

    def add(self, *systems: Type[_TS]) -> None:
        for system in systems:
            self._add(system)

    def _add(self, system: Type[_TS]) -> None:
        self._systems[system.system_tag()].add(system(self._app))

    def by_system(self, system_type: Type[_TS]) -> Iterable[_TS]:
        return self._systems[system_type.system_tag()].__iter__()
