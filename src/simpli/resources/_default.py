from simpli.resources._holder import ResourceHolder
from simpli.resources._resource import Resource


class DefaultResourceHolder(ResourceHolder):
    def __init__(self) -> None:
        self._resources: dict[str, Resource] = {}

    def add(
            self,
            resource: Resource,
    ) -> None:
        self._resources[resource.tag()] = resource

    def get[T: Resource](
            self,
            resource: type[T]
    ) -> T:
        try:
            return self._resources[resource.tag()]
        except KeyError:
            raise RuntimeError("Unable to get resource")

    def find[T: Resource](
            self,
            resource: type[T]
    ) -> T | None:
        try:
            return self._resources[resource.tag()]
        except KeyError:
            return None

    def has(
            self,
            resource: type[Resource]
    ) -> bool:
        return resource.tag() in self._resources

    def remove(
            self,
            resource: type[Resource],
    ) -> None:
        self._resources.pop(resource.tag(), None)
