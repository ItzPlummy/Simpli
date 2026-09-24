from abc import ABC, abstractmethod

from simpli.resources._resource import Resource


class ResourceHolder(ABC):
    @abstractmethod
    def add(
            self,
            resource: Resource,
    ) -> None:
        ...

    @abstractmethod
    def get[T: Resource](
            self,
            resource: type[T]
    ) -> T:
        ...

    @abstractmethod
    def find[T: Resource](
            self,
            resource: type[T]
    ) -> T | None:
        ...

    @abstractmethod
    def has(
            self,
            resource: type[Resource],
    ) -> bool:
        ...

    @abstractmethod
    def remove(
            self,
            resource: type[Resource],
    ) -> None:
        ...

    def __getitem__(
            self,
            resource: type[Resource],
    ) -> Resource | None:
        return self.get(resource)

    def __contains__(
            self,
            resource: type[Resource],
    ) -> bool:
        return self.has(resource)
