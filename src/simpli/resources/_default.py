from typing import Dict

from simpli.resources._holder import ResourceHolder
from simpli.resources._resource import Resource


class DefaultResourceHolder(ResourceHolder):
    __slots__ = ("_resources",)

    def __init__(self) -> None:
        self._resources: Dict[str, Resource] = {}

    def add(self, resource: Resource) -> None:
        self._resources[resource.tag()] = resource

    def get(self, resource_tag: str) -> Resource | None:
        return self._resources.get(resource_tag)

    def has(self, resource_tag: str) -> bool:
        return resource_tag in self._resources

    def remove(self, resource_tag: str) -> None:
        self._resources.pop(resource_tag)
