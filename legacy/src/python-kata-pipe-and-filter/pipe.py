import itertools

class Pipe:
    def __init__(self, seq):
        self._seq = seq

    def __iter__(self):
        return iter(self._seq)
    
    def map(self, func):
        return Pipe(map(func, self))

    def flat_map(self, func=None):
        maped = self if func is None else map(func, self)
        return Pipe(itertools.chain.from_iterable(maped))

    def filter(self, func=None):
        return Pipe(filter(func, self))
