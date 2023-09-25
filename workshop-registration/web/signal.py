
class Signal:
    def __init__(self) -> None:
        self._funs = set()

    def connect(self, fun) -> None:
        self._funs.add(fun)

    def send(self, *args, **kwargs) -> None:
        for fun in self._funs:
            fun(*args, **kwargs)