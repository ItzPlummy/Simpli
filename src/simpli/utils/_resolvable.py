from simpli.utils._binding import Binding


type Resolvable[T] = T | Binding[T]


def resolve[T](resolvable: Resolvable[T]) -> T:
    return resolvable() if isinstance(resolvable, Binding) else resolvable
