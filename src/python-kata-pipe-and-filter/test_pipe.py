import unittest
from unittest import mock
from pipe import Pipe

class TestPipe(unittest.TestCase):
    
    def test_Should_IterateOverTheSameSequence_When_Created(self):
        input = [2,3,4]
        pipe = Pipe(input)
        result = [x for x in pipe]
        self.assertEqual(input, result)

    def test_Should_ReturnMappedVlaues_When_MapApplied(self):
        input = [7,8,9]
        func = lambda x: -x
        pipe = Pipe(input).map(func)
        result = [x for x in pipe]
        self.assertEqual([-7,-8,-9], result)

    def test_Should_ReturnMappedFlattenedValues_When_FlatMapApplied(self):
        input = ['Lorem ipsum', 'dolorem costum']
        func = lambda x: x.lower().split(' ')
        pipe = Pipe(input).flat_map(func)
        result = [x for x in pipe]
        self.assertEqual(['lorem', 'ipsum', 'dolorem', 'costum'], result)

    def test_Should_DropFilteredOutValues_When_FilterApplied(self):
        input = [-1, 3, -6, 5]
        func = lambda x: x >= 0
        pipe = Pipe(input).filter(func)
        result = [x for x in pipe]
        self.assertEqual([3,5], result)

if __name__ == "__main__":
    unittest.main(argv=[__file__,'-vv'])
