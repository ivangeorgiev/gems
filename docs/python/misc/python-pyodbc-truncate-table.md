---
tags: python, pyodbc, tdd
creatrd: 2020-08-17
---

# Truncate table with pyodbc

## Problem

You need to truncate a table using `pyodbc`. 

## Solution

Here is an example of a function to truncate a database table, using `pyodbc` connection.

You can find the full source in [GitHub](https://github.com/ivangeorgiev/gems/src/pyodbc_truncate_table).

```python
def truncate_table(table_ref, dbc):
    try:
        with dbc.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {table_ref}')
            cursor.commit()
    except Exception as err:
        dbc.rollback()
        raise err
```

### Testing the solution

Although the function is simple, it needs testing. The function should perform two steps:

1. Truncate the table, executing `TRUNCATE TABLE` sql statement
2. Commit the transaction

This is the happy flow.

In addition to the happy flow there is an exception flow which happens when pyodbc fails to execute the `TRUNCATE TABLE` sql statement.

Here is a sample implementation of the unit tests that cover above scenarios.

```python
import unittest
from unittest import mock
from pyodbc_functions import truncate_table

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

    def test_truncate_table_calls_rollback_on_and_propagates_exception_given_database_execute_fails(self):
        dbc = self.fix_dbc()

        with dbc.cursor() as cursor:
            cursor.execute.side_effect = Exception('bad boy')
            with self.assertRaises(Exception) as excinfo:
                truncate_table('users', dbc)
            self.assertEqual('bad boy', str(excinfo.exception))
            cursor.asset_has_calls([
                mock.call.execute(mock.call.ANY),
                mock.call.rollback()
            ])

```

We use mock database connection.

In the happy flow test we pass mock database connection to the `truncate_table` function. Once the function is executed, we assert that following steps were made in a sequence:

1. `execute` was called on the database cursor with proper SQL statement as argument
2.  `commit` with no arguments was called on the database cursor.

In the exception flow test, we again use a mock database connection, but this time we configure the `execute` method of the cursor to throw an exception. 

We make sure the exception is propagated with `assertRaises()` unittest assert. We also check that the message of the exception is preserved.

We verify that the flow is calling:

1. `execute` method of the cursor - we do not verify the arguments since we already validated this in the happy flow.
2. `rollback` method on the database connection.

## Discussion

You can call the `execute` method on a connection cursor directly, but it is always better to move the code into a separate routine:

* provides reusability - you have a tested piece of code that can be used everywhere.
* improves the readability of the code - you create your own idioms or dictionary which make your code more expressive.
* improves the testability of the code - imagine your code truncates the table in the middle of 200+ line code fragment. How would you test it works correctly? How would you cover both scenarios?
* isolates your code from the external system - one of the benefits of this isolation is that you can unit test your code.