import unittest
from unittest import mock
import sys
import os
from ..pyodbc_functions import truncate_table



class Test_function_truncate_table(unittest.TestCase):

    def fix_dbc(self):
        dbc = mock.MagicMock()
        return dbc

    def test_truncate_table_calls_proper_methods_given_database_execute_is_successful(self):
        dbc = self.fix_dbc()

        truncate_table('users', dbc)
        with dbc.cursor() as cursor:
            cursor.assert_has_calls([
                mock.call.execute('TRUNCATE TABLE users'),
                mock.call.commit()
            ])

    def test_truncate_table_calls_rollback_and_propagates_exception_given_database_execute_fails(self):
        dbc = self.fix_dbc()

        with dbc.cursor() as cursor:
            cursor.execute.side_effect = Exception('bad boy')
            with self.assertRaises(Exception) as excinfo:
                truncate_table('users', dbc)
            self.assertEqual('bad boy', str(excinfo.exception))
        cursor.execute.assert_called_once_with(mock.ANY)
        dbc.rollback.assert_called_once()
