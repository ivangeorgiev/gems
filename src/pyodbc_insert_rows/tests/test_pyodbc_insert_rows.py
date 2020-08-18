import unittest
from unittest import mock
from ..pyodbc_insert_rows import insert_rows

class Test_function_insert_rows(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0], '-v'])
