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


p = Pipe([1,2,3]).map(lambda x: 'x'*x).flat_map()
# .flat_map(lambda x: 'x'*x)
for x in p:
    print(x)

pipe = (Pipe([4,6,9])
        .map(lambda x: int(x/2))
        .flat_map(lambda x: [x]*x))
for item in pipe:
    print(item)