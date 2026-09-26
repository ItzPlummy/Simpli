from typing import Callable, ClassVar


class Binding[T]:
    __slots__ = ("_epoch", "_binding", "_value")

    _CACHING: ClassVar[bool] = False
    _EPOCH: ClassVar[int] = -1

    def __init__(
            self,
            binding: Callable[[], T],
    ) -> None:
        if not callable(binding):
            raise TypeError("Binding argument must be callable")

        self._epoch: int = -1
        self._binding: Callable[[], T] = binding
        self._value: T = None

    @classmethod
    def begin_scope(cls) -> None:
        cls._CACHING = True
        cls._EPOCH += 1

    @classmethod
    def end_scope(cls) -> None:
        cls._CACHING = False

    @property
    def binding(self) -> Callable[[], T]:
        return self._binding

    def __call__(self) -> T:
        if not Binding._CACHING:
            return self.binding()

        if self._epoch != Binding._EPOCH:
            self._value = self.binding()
            self._epoch = Binding._EPOCH

        return self._value
