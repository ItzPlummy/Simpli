from abc import ABC
from typing import dataclass_transform, Any

from pydantic.dataclasses import dataclass


@dataclass_transform(kw_only_default=True)
class Component(ABC):
    def __init_subclass__(
            cls,
            **kwargs: Any,
    ) -> None:
        super().__init_subclass__()

        kwargs.update(
            {
                "kw_only": True
            }
        )

        dataclass(cls, **kwargs)
