from simpli.utils._supplier import Supplier


type Resolvable[T] = T | Supplier[T]


def resolve[T](resolvable: Resolvable[T]) -> T:
    return resolvable() if callable(resolvable) else resolvable
