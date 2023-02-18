import unittest
from unittest import mock

from ..pyodbc_helpers import *



class Test_module_pyodbc_helpers(unittest.TestCase):

    def fix_dbc(self):
        dbc = mock.MagicMock(spec=['cursor', 'autocommit', 'rollback'])
        dbc.autocommit = True
        dbc.cursor.return_value.__enter__.return_value = mock.MagicMock(spec=['execute', 'commit', 'executemany', 'rollback'])

        return dbc

    def fix_rows(self):
        rows = [{'id':1, 'name':'John'}, 
                {'id':2, 'name':'Jane'},]
        return rows

    def fix_tuples(self):
        tuples = [(1,'John'),
                  (2,'Jane'),]
        return tuples

    def test_insert_rows_calls_cursor_context_manager(self):
        dbc = self.fix_dbc()
        rows = self.fix_rows()
        insert_rows(rows, 'users', dbc)
        self.assertTrue(dbc.cursor.called)
        self.assertTrue(dbc.cursor.return_value.__enter__.called)


    def test_insert_rows_calls_executemany_and_commit(self):
        dbc = self.fix_dbc()
        rows = self.fix_rows()

        insert_rows(rows, 'users', dbc)

        with dbc.cursor() as cursor:
            expect_sql = 'INSERT INTO users(id, name) VALUES (?,?)'
            expect_tuples = self.fix_tuples()
            calls = [mock.call.executemany(expect_sql, expect_tuples),
                     mock.call.commit(),]
            cursor.assert_has_calls(calls)
        self.assertTrue(dbc.autocommit)

    def test_insert_rows_rollsback_transaction_and_propagates_exception_given_database_execution_fails(self):
        dbc = self.fix_dbc()
        rows = self.fix_rows()

        with dbc.cursor() as cursor:
            cursor.executemany.side_effect = Exception('Some DB error')

            with self.assertRaises(Exception) as exc:
                insert_rows(rows, 'users', dbc)

            self.assertEqual('Some DB error', str(exc.exception))
            
            calls = [mock.call.executemany(mock.ANY, mock.ANY),
                     mock.call.rollback(),]
            cursor.assert_has_calls(calls)
        self.assertTrue(dbc.autocommit)


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

    def test_convert_rows_with_no_converter_returns_list_of_namedtuple(self):
        cursor = mock.Mock(spec=['x'])
        cursor.description = [('id',), ('name',)]
        rows = [(1,'John'), (2, 'Jane')]
        result = convert_rows(rows, cursor)
        self.assertIsInstance(result, list)
        self.assertEqual({'id':1, 'name': 'John'}, result[0]._asdict())

    def test_convert_rows_with_converter_returns_list_of_convertor_results(self):
        cursor = mock.Mock(spec=['x'])
        cursor.description = [('id',), ('name',)]
        rows = [(1,'John'), (2, 'Jane')]
        result = convert_rows(rows, cursor, dict)
        self.assertIsInstance(result, list)
        self.assertEqual([{'id':1, 'name': 'John'}, {'id':2, 'name':'Jane'}], result)
