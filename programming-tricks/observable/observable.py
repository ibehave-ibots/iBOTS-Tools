from typing import Callable, Optional, Set, TypeVar, Generic


class Signal:
    """
    Signals are responsible for connecting obesrvables and observers, passing data from one to the other.
    
    Signal.connect() registers an observer function.
    Signal.send(args, kwargs) calls all registered observer functions with the args and kwargs.
    """
    def __init__(self) -> None:
        self._funs: Set[Callable] = set()

    def connect(self, fun) -> None:
        self._funs.add(fun)

    def send(self, *args, **kwargs) -> None:
        for fun in self._funs:
            fun(*args, **kwargs)


T = TypeVar('T')


class Observable(Generic[T]):
    """
    The Observable sends an "updated" Signal whenever its data attribute is updated.
    It's useful for managing state of immutable data.
    """
    updated: Signal

    def __init__(self, data: T, updated: Optional[Signal] = None):
        self._data = data
        self.updated: Signal = updated if updated else Signal()

    def send_all(self) -> None:
        self.updated.send(self._data)

    @property
    def data(self) -> T:
        return self._data
    
    @data.setter
    def data(self, value: T) -> None:
        self._data = value
        self.updated.send(self._data)