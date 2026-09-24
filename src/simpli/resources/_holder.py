from abc import ABC, abstractmethod
from typing import Any

from simpli.resources._resource import Resource


class ResourceHolder(ABC):
    @abstractmethod
    def add(
            self,
            resource: Resource,
    ) -> None:
        ...

    @abstractmethod
    def get(
            self,
            resource_tag: str,
    ) -> Resource | None:
        ...

    @abstractmethod
    def has(
            self,
            resource_tag: str,
    ) -> bool:
        ...

    @abstractmethod
    def remove(
            self,
            resource_tag: str,
    ) -> None:
        ...

    def __getitem__(
            self,
            item: Any,
    ) -> Resource | None:
        return self.get(str(item))

    def __contains__(
            self,
            item: Any,
    ) -> bool:
        return self.has(str(item))
