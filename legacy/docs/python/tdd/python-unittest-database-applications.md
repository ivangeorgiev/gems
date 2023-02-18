---
tags: python, tdd
date: 2020-04-14 16:40:00
---



# Unit testing for Python database applications

## Problem

You are building an application that uses database in Python. For example, you might have created following function, which uses pyodbc to insert a list of rows into a database table. Each row is a dictionary.

```python
def insert_rows(rows, table_name, dbc):
    field_names = rows[0].keys()
    field_names_str = ', '.join(field_names)
    placeholder_str = ','.join('?'*len(field_names))
    insert_sql = f'INSERT INTO {table_name}({field_names_str}) VALUES ({placeholder_str})'
    saved_autocommit = dbc.autocommit
    with dbc.cursor() as cursor:
        try:
            dbc.autocommit = False
            tuples = [ tuple((row[field_name] for field_name in field_names)) for row in rows ]
            cursor.executemany(insert_sql, tuples)
            cursor.commit()
        except Exception as exc:
            cursor.rollback()
            raise exc
        finally:
            dbc.autocommit = saved_autocommit
```

How I can unit test such a function?

## Solution

Use `unittest.mock` to generate mock database connection. It is as simple as:

```python
dbc = mock.MagicMock()
```

The very first test could be to verify that our function calls the `cursor()` method of the database connection.

```python
import unittest
from unittest import mock


class Test_insert_rows(unittest.TestCase):

    def fix_dbc(self):
        dbc = mock.MagicMock(spec=['cursor'])
        dbc.autocommit = True
        return dbc

    def fix_rows(self):
        rows = [{'id':1, 'name':'John'}, 
                {'id':2, 'name':'Jane'},]
        return rows

    def test_insert_rows_calls_cursor_method(self):
        dbc = self.fix_dbc()
        rows = self.fix_rows()
        insert_rows(rows, 'users', dbc)
        self.assertTrue(dbc.cursor.called)

if __name__ == '__main__':
    unittest.main(argv=['', '-v'])

```

Some highlights on what I have done in this test:

* The database connection, used for testing is created using a method. This is because I am gonna need this connection again and again in the test methods I am going to create.
* The rows fixture is also created using a method. For the same reason.
* At the end there is `if __name__ == '__main__':...` . This will run `unittest` if I execute the file as python script.

Here is the result of the execution:

```
(.venv37) sandbox>python test_insert_rows.py -v
test_insert_rows_calls_cursor_method (test_insert_rows.Test_insert_rows) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.002s

OK
```



The test I have created so far is not very exciting. To create a better test, let's look closely at what this function does:

- generates insert statement
- generates a list of tuples from the rows list
- calls the `executemany` method of the database cursor
- commits the transaction

So my test could verify that the function calls the `executemany` method with correct arguments and commits the transaction.

Let's implement this test.

```python
    def fix_tuples(self):
        tuples = [(1,'John'),
                  (2,'Jane'),]
        return tuples

    def test_insert_rows_calls_executemany_and_commit_passing_correct_arguments(self):
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

```

In this test I use the `assert_has_calls` assertion of the mock object to verify that specific calls has been made with expected arguments and in expected order.

At the end of the test I verify that `autocommit` property of the database connection is restored to `True`.

Ok. Great. So far we tested the happy path. What happens if something fails?

In the following test I am gonna make the database connection raise an exception to test the behavior of  my function. We have to verify:

* Transaction is rolled back after `executemany` is called.
* Database connection `autocommit` property has been restored.
* Exception is propagated.

```python
    def test_insert_rows_rollsback_transaction_on_databse_exception(self):
        dbc = self.fix_dbc()
        rows = self.fix_rows()

        with dbc.cursor() as cursor:
            cursor.executemany.side_effect = Exception('Some DB error')

            with self.assertRaises(Exception) as exc:
                insert_rows(rows, 'users', dbc)

            calls = [mock.call.executemany(mock.ANY, mock.ANY),
                     mock.call.rollback(),]
            cursor.assert_has_calls(calls)
        self.assertTrue(dbc.autocommit)
        self.assertEqual('Some DB error', str(exc.exception))
```



## Discussion

It might seem easier using real database, but it has drawbacks:

* Actual database might not be available or you might not have connectivity to it.
* You are not testing your code in isolation. If, for example, the database connection is unstable, you will start getting wired, unpredictable results.
* Database requests add significant latency.
* You need to reset the database state before each state to a fixed well-known state. This might be challenging, especially if the database is shared.

Looking at our function, we could see a smell. It does more than one thing:

1. Generate INSERT statement
2. Generate tuples list
3. Insert the tuples into the database

There are also some conditions that might have been handled better. What if I pass empty list of rows?

The good news is, we could refactor our code and make sure our code still works properly. We know we haven't broken anything. Just because we have thorough unit tests.

## Refactoring - Extract function

Let's move the code for generating INSERT statement into a new function. We are going to follow these steps:

1. Run our tests and make sure they pass (green).
2. Create a test the new function.
3. Run our tests and make sure they fail (red).
4. Create a new function and copy the code we want to extract.
5. Run our tests and make sure they pass (green).
6. Replace the old code with a call to the new function.
7. Run our tests and make sure they still pass (green).

Let's implement the test:

```python
    def test_make_insert_produces_correct_statement(self):
        
        fields = ['id', 'name']
        actual = make_insert_statement(fields, 'users')

        expected = 'INSERT INTO users(id, name) VALUES (?,?)'
        self.assertEqual(expected, actual)
```

Tests are failing now:

```
(.venv37) sandbox>python test_insert_rows.py
test_insert_rows_calls_cursor_method (__main__.Test_insert_rows) ... ok
test_insert_rows_calls_executemany_and_commit_passing_correct_arguments (__main__.Test_insert_rows) ... ok
test_insert_rows_rollsback_transaction_on_databse_exception (__main__.Test_insert_rows) ... ok
test_make_insert_produces_correct_statement (__main__.Test_insert_rows) ... ERROR

======================================================================
ERROR: test_make_insert_produces_correct_statement (__main__.Test_insert_rows)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "c:/Sandbox/Learn/Python/TestDrivenPythonDevelopment/play/sandbox/test_insert_rows.py", line 42, in test_make_insert_produces_correct_statement     
    actual = make_insert_statement(fields, 'users')
NameError: name 'make_insert_statement' is not defined

----------------------------------------------------------------------
Ran 4 tests in 0.017s

FAILED (errors=1)
```

Now we implement the function:

```python
def make_insert_statement(field_names, table_name):
    field_names_str = ', '.join(field_names)
    placeholder_str = ','.join('?'*len(field_names))
    insert_sql = f'INSERT INTO {table_name}({field_names_str}) VALUES ({placeholder_str})'
    return insert_sql
```

Tests are passing.

We update the `insert_rows` function to call the new `make_insert_statement` function and run the tests to see them passing.

```python
def insert_rows(rows, table_name, dbc):
    field_names = rows[0].keys()
    insert_sql = make_insert_statement(field_names, table_name)
    saved_autocommit = dbc.autocommit
    with dbc.cursor() as cursor:
        try:
            dbc.autocommit = False
            tuples = [ tuple((row[field_name] for field_name in field_names)) for row in rows ]
            cursor.executemany(insert_sql, tuples)
            cursor.commit()
        except Exception as exc:
            cursor.rollback()
            raise exc
        finally:
            dbc.autocommit = saved_autocommit
```

The new version of the function is not much shorter, but has some advantages:

* improved readability - it is much easier to understand what the code is doing
* improved reusability - it is very likely that we might need the INSERT statement generation in another situation
* better testability - we could test the generation of the INSERT statement in isolation. Introducing new test cases for this functionality is easy. It doesn't require database connection, for example.

If we follow the principles of the test driven development (TDD), we should remove the check for the generated statement in the call to the `insertmany`.  We could achieve this by patching the `make_insert_statement` function.

```python
    @mock.patch('__main__.make_insert_statement')
    def test_insert_rows_calls_executemany_and_commit_passing_correct_arguments(self, make_insert_mock):
        dbc = self.fix_dbc()
        rows = self.fix_rows()
        
        make_insert_mock.return_value = 'MY PRECIOUS'

        insert_rows(rows, 'users', dbc)

        with dbc.cursor() as cursor:
            expect_sql = 'MY PRECIOUS'
            expect_tuples = self.fix_tuples()
            calls = [mock.call.executemany(expect_sql, expect_tuples),
                     mock.call.commit(),]
            cursor.assert_has_calls(calls)
        self.assertTrue(dbc.autocommit)
```

Wait! What is going here? 

I used the `patch` decorator to replace the `make_insert_statement` with a mock object. The mock object is automatically added as second argument to my test method.

I have also defined that the `make_insert_statement` mock returns a fixed value `MY PRECIOS`. It is not valid SQL, but our mock database connection doesn't care. The important thing is that we see the result from the `make_insert_statement` passed to the `executemany` method.