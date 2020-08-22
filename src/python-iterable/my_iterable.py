

class MyIterable:
    def __init__(self, items):
        self._items = items

    def _iterate(self):
        for x in self._items:
            yield x

    def __iter__(self):
        return self._iterate()


class GeneratorInIter:
    def __init__(self, items):
        self._items = items

    def __iter__(self):
        for item in self._items:
            yield item
