from abc import ABC
from typing import Any, ClassVar, Iterable


class System(ABC):
    _KINDS: ClassVar[set[type[System]]] = set()

    def __init_subclass__(
            cls,
            *,
            is_kind: bool = False,
            **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)

        if is_kind:
            System._KINDS.add(cls)

    @classmethod
    def get_kinds(cls) -> Iterable[type[System]]:
        return cls._KINDS
