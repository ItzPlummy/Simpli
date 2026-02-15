from typing import TypeVar, Callable, Generic, Any, TYPE_CHECKING

_T = TypeVar("_T", bound=object)


if TYPE_CHECKING:
    class Value(Generic[_T], _T):
        pass
else:
    class Value(Generic[_T]):
        def __init__(self, value: _T | Callable[[], _T]) -> None:
            if callable(value):
                self._v: Callable[[], _T] = value
            else:
                self._v: Callable[[], _T] = lambda: value

        @property
        def value(self) -> _T:
            try:
                return self._v()
            except TypeError:
                raise ValueError("Callable must not accept args")

        def __getattr__(self, name: str) -> Any:
            return getattr(self.value, name)

        def __getitem__(self, key: Any) -> Any:
            return self.value[key]

        def __setitem__(self, key: Any, value: Any) -> None:
            self.value[key] = value

        def __delitem__(self, key: Any) -> None:
            del self.value[key]

        def __len__(self) -> int:
            return len(self.value)

        def __contains__(self, item: Any) -> bool:
            return item in self.value

        def __str__(self) -> str:
            return str(self.value)

        def __repr__(self) -> str:
            return repr(self.value)

        def __bool__(self) -> bool:
            return bool(self.value)

        def __eq__(self, other: Any) -> bool:
            return self.value == (other.value if isinstance(other, Value) else other)

        def __ne__(self, other: Any) -> bool:
            return not self == other

        def __lt__(self, other: Any) -> bool:
            return self.value < (other.value if isinstance(other, Value) else other)

        def __le__(self, other: Any) -> bool:
            return self.value <= (other.value if isinstance(other, Value) else other)

        def __gt__(self, other: Any) -> bool:
            return self.value > (other.value if isinstance(other, Value) else other)

        def __ge__(self, other: Any) -> bool:
            return self.value >= (other.value if isinstance(other, Value) else other)

        def __neg__(self) -> Any:
            return -self.value

        def __pos__(self) -> Any:
            return +self.value

        def __invert__(self) -> Any:
            return ~self.value

        def __abs__(self) -> Any:
            return abs(self.value)

        def __add__(self, other: Any) -> Any:
            return self.value + other.value if isinstance(other, Value) else other

        def __radd__(self, other: Any) -> Any:
            return other.value if isinstance(other, Value) else other + self.value

        def __sub__(self, other: Any) -> Any:
            return self.value - (other.value if isinstance(other, Value) else other)

        def __rsub__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) - self.value

        def __mul__(self, other: Any) -> Any:
            return self.value * (other.value if isinstance(other, Value) else other)

        def __rmul__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) * self.value

        def __truediv__(self, other: Any) -> Any:
            return self.value / (other.value if isinstance(other, Value) else other)

        def __rtruediv__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) / self.value

        def __floordiv__(self, other: Any) -> Any:
            return self.value // (other.value if isinstance(other, Value) else other)

        def __rfloordiv__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) // self.value

        def __mod__(self, other: Any) -> Any:
            return self.value % (other.value if isinstance(other, Value) else other)

        def __rmod__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) % self.value

        def __pow__(self, other: Any, modulo: Any = None) -> Any:
            return pow(self.value, (other.value if isinstance(other, Value) else other), modulo)

        def __rpow__(self, other: Any) -> Any:
            return pow((other.value if isinstance(other, Value) else other), self.value)

        def __and__(self, other: Any) -> Any:
            return self.value & (other.value if isinstance(other, Value) else other)

        def __rand__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) & self.value

        def __or__(self, other: Any) -> Any:
            return self.value | (other.value if isinstance(other, Value) else other)

        def __ror__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) | self.value

        def __xor__(self, other: Any) -> Any:
            return self.value ^ (other.value if isinstance(other, Value) else other)

        def __rxor__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) ^ self.value

        def __lshift__(self, other: Any) -> Any:
            return self.value << (other.value if isinstance(other, Value) else other)

        def __rlshift__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) << self.value

        def __rshift__(self, other: Any) -> Any:
            return self.value >> (other.value if isinstance(other, Value) else other)

        def __rrshift__(self, other: Any) -> Any:
            return (other.value if isinstance(other, Value) else other) >> self.value
