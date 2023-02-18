import unittest
from unittest import mock
from repeater import Repeater

class TestException(Exception):
    pass

class RepeaterTest(unittest.TestCase):

    def assertIsIterable(self, o):
        try:
            iter(o)
        except:
            self.fail('Not iterable')

    def test_Should_ReturnInstance_When_Created(self):
        repeater = Repeater('hello')
        self.assertIsIterable(repeater)

    def test_Should_ReturnStaticValue_When_CreatedWithNonCallable(self):
        value = 'hello'
        repeater = Repeater(value)
        result = []
        result.append(next(repeater))
        result.append(next(repeater))
        self.assertEqual([value, value], result)

    def test_Should_ReturnResultFromCall_When_CreatedWithCallable(self):
        func = mock.Mock(spec=[])
        func.side_effect = [1, 2, 3]
        repeater = Repeater(func)
        result = []
        result.append(next(repeater))
        result.append(next(repeater))
        self.assertEqual([1, 2], result)

    def test_Should_Stop_When_FunctionRaisesStopIteration(self):
        func = mock.Mock(spec=[])
        func.side_effect = [1, 2, StopIteration]
        repeater = Repeater(func)
        result = []
        for x in repeater:
            result.append(x)
        self.assertEqual([1, 2], result)

    def test_Should_PropagateExceptionFromFunction_When_FunctionRaisesException(self):
        func = mock.Mock(spec=[])
        func.side_effect = [1, 2, TestException]
        repeater = Repeater(func)
        next(repeater)
        next(repeater)
        with self.assertRaises(TestException):
            next(repeater)



if __name__ == "__main__":
    unittest.main(argv=[__file__,'-vv'])

 