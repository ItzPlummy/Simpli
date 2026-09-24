from typing import Callable


type Supplier[T] = Callable[[], T]
