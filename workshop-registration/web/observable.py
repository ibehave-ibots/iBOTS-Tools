from typing import TypeVar, Generic


class Signal:
    def __init__(self) -> None:
        self._funs = set()

    def connect(self, fun) -> None:
        self._funs.add(fun)

    def send(self, *args, **kwargs) -> None:
        for fun in self._funs:
            fun(*args, **kwargs)


T = TypeVar('T')


class Observable(Generic[T]):
    updated: Signal

    def __init__(self, data: T, updated: Signal = None):
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