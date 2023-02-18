import unittest
from unittest import mock
from collections import namedtuple
from read_csv import get_file_lines, read_csv

class TestGetFileLines(unittest.TestCase):
    
    def test_Should_ExitTheWithBock_When_IterationExhausted(self):
        with mock.patch('builtins.open', mock.MagicMock()) as m_open:
            lines = get_file_lines('myfile')
            try:
                next(lines)
            except StopIteration:
                pass
        self.assertTrue(m_open.return_value.__exit__.called)

    def test_Should_IterateOverFileLines_When_Iterated(self):
        with mock.patch('builtins.open', mock.MagicMock()) as m_open:
            m_open.return_value.__enter__.return_value = [1,2]
            result = list(get_file_lines('myfile'))
            self.assertEqual([1,2], result)


class TestReadCsv(unittest.TestCase):

    def test_Should_ReturnIteratorOverNamedTupleRows_When_Called(self):
        with mock.patch('read_csv.get_file_lines', mock.MagicMock()) as m_get_file_lines:
            m_get_file_lines.return_value = ['id,name', '1,John']
            result = list(read_csv('myfile'))

            Row = namedtuple('Row', 'id,name')
            expected = [Row('1', 'John')]
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main(argv=[__file__,'-vv'])
