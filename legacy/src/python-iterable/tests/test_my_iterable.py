import unittest
from ..my_iterable import MyIterable, GeneratorInIter

class IterableTest(unittest.TestCase):

    def test_hi(self):
        team = MyIterable(['John', 'Jane'])
        values = []
        for member in team:
            values.append(member)
        self.assertEqual(['John', 'Jane'], values)

    def test_GeneratorInIter(self):
        team = GeneratorInIter(['John', 'Jane'])
        values = []
        for member in team:
            values.append(member)
        self.assertEqual(['John', 'Jane'], values)

 