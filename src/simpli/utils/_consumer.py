from typing import Callable


type Consumer[T] = Callable[[T], None]
