

class Signal:

    def __init__(self) -> None:
        self._ports = []

    def connect(self, fun):
        self._ports.append(fun)

    def send(self, *args, **kwargs):
        for fun in self._ports:
            fun(*args, **kwargs)
