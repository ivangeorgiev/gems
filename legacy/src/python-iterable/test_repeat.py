import unittest
from unittest import mock
from repeat import repeat

class TestException(Exception):
    pass

class Repeat_Function_Test(unittest.TestCase):

    def test_Should_CallFunctionUntilStopIterationException_When_Called(self):
        func = mock.Mock(spec=[])
        func.side_effect = [ [1], [2], StopIteration ]
        called_history = []
        for _ in repeat(func):
            called_history.append(func.called)
            func.called = False
        self.assertEqual([True, True], called_history)

    def test_Should_PropagateFunctionException_When_ExceptionRaised(self):
        func = mock.Mock(spec=[])
        func.side_effect = [ TestException ]
        called_history = []
        with self.assertRaises(TestException):
            for _ in repeat(func):
                pass

    def test_Should_CallBeforeBeforeYielding_When_BeforeSpecified(self):
        func = mock.Mock(spec=[])
        before = mock.Mock(spec=[])
        func.side_effect = [ 1, StopIteration ]
        for _ in repeat(func, before=before):
            self.assertTrue(before.called)

    def test_Should_NotCallAfterBeforeYielding_When_AfterSpecified(self):
        func = mock.Mock(spec=[])
        after = mock.Mock(spec=[])
        func.side_effect = [ 1, StopIteration ]
        for _ in repeat(func, after=after):
            self.assertFalse(after.called)

    def test_Should_CallAfterAfterYielding_When_AfterSpecified(self):
        func = mock.Mock(spec=[])
        after = mock.Mock(spec=[])
        func.side_effect = [ 1, StopIteration ]
        for _ in repeat(func, after=after):
            pass
        self.assertTrue(after.called)

