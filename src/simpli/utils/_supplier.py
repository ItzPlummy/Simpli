from typing import Callable


class Supplier[T]:
    __slots__ = ("_supplier",)

    def __init__(
            self,
            supplier: Callable[[], T],
    ) -> None:
        if not callable(supplier):
            raise TypeError("Supplier must be callable")

        self._supplier: Callable[[], T] = supplier

    def __call__(self) -> T:
        return self._supplier()
