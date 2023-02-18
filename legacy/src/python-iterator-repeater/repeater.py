
class Repeater:

    def __init__(self, value):
        if callable(value):
            self._value = value
        else:
            self._value = lambda: value

    def __iter__(self):
        return self

    def __next__(self):
        return self._value()
