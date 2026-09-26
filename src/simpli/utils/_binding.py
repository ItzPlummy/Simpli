from typing import Callable


class Binding[T]:
    __slots__ = ("_binding",)

    def __init__(
            self,
            binding: Callable[[], T],
    ) -> None:
        if not callable(binding):
            raise TypeError("Binding argument must be callable")

        self._binding: Callable[[], T] = binding

    def __call__(self) -> T:
        return self._binding()
