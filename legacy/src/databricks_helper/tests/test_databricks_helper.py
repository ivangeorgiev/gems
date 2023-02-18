import unittest
from unittest import mock
from collections import namedtuple
from ..databricks_helper import *

FileInfo = namedtuple('FileInfo', 'name,path,size')
class TestModule_databricks_helper(unittest.TestCase):
    
    def fix_dbutils(self):
        dbutils = mock.Mock(spec=['fs'])
        dbutils.fs = mock.Mock(spec=['ls'])
        return dbutils

    def test_ls_matching_returns_list_of_matching_files_if_match(self):
        dbutils = self.fix_dbutils()
        data = [FileInfo('/path/to/aaa.txt', 'aaa.txt', 100),
                FileInfo('/path/to/aba.json', 'aba.json', 100),
                FileInfo('/path/to/baa.txt', 'baa.txt', 100)]
        path = '/path/to'
        pattern = 'a*.txt'
        dbutils.fs.ls.return_value = data

        result = ls_matching(path, pattern)
        expect = data[0]._asdict()
        actual = result[0]._asdict()
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual(expect, actual)
