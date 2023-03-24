# Mock Python Context Manager

## Python Context Manager in a Nutshell

Python context manager protocol requires that object used as context manager implements two methods:

* `__enter__` - this method is called when the control is transferred to the context - at the beginning of the `with` block.
* `__exit__` - this method is called when the execution of the context is complete - after the `with` block.

```python

class fake_customer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("Entering fake_customer context")
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting fake_customer context")

with fake_customer('John') as customer:
    print(f"Hello {customer}")

```

Above code produces output similar to the following:

```
Entering fake_customer context
Hello John
Exiting fake_customer context
```

## Creating a Mock Context Manager

We need that our mock manager returns particular value. To satisfy the context manager protocol, we provide the mock_manager object a method `__enter__` with return value:

```python
from unittest.mock import Mock

context_value = Mock()

mock_manager = Mock()
mock_manager.__enter__.return_value = context_value
```

## Function Which Returns Context Manager

Let's say we have a function `db_connect` which returns a context manager which maintains a database connection.

```python
mock_connection = Mock()
# ... setup the connection mock here ...

db_connect_mock = Mock()
db_connect_mock.return_value.__enter__.return_value = mock_connection

with patch('db_connect', db_connect_mock):
    get_customer('johndoe')
```

The `get_customer` function will call the `db_connect` function and receive a mock database
connection manager. The mock database connection manager returns the `mock_connection` we built.

## Example: Mock Python's `open` Function

In the following example we are testing a Python function `readFileFirstLine` which returns the first line from a file with given name.

The `readFileFirstLine` uses the `open()` function and `with` statement context manager. In order to test our function in isolation, we need to:

1. Create a stub file \
   ```python
   mock_file = Mock()
   mock_file.readline.return_value = "test line"
   ```
2. Create a mock context manager with `__enter__` method which returns the stub file \
   ```python
   mock_context_manager = Mock()
   mock_context_manager.__enter__.return_value = mock_file
   ```
2. Replace (patch) the `open` context manager with a stub that returns a mock context manager
   ```python
   mock_open = Mock(return_vaulue=mock_context_manager)
   ```

To verify the  function behaves correctly we need to make sure that `open` was called with proper arguments  and  that the `readFileFirstLine` function returns the value acquired from the `file`'s `readline()` method.

Here is a sample implementation of the complete test case:

```python

from unittest import TestCase
from unittest.mock import Mock, patch

def readFromFile(filename):
    with open(filename, "r", encoding="utf8") as f:
        return f.readline()

class TestReadFromFileFunction(TestCase):
    def test_returns_correct_string(self):
        # Setup
        mock_file = Mock()
        mock_file.readline.return_value = "test line"

        mock_context_manager = Mock()
        mock_context_manager.__enter__.return_value = mock_file

        mock_open = Mock(return_value=mock_context_manager)

        # Act
        with patch("builtins.open", mock_open):
            result = readFileFirstLine("blah")

        # Assert
        mock_open.assert_called_once_with("blah", "r", encoding="utf8")
        self.assertEqual(result, "first line")
```

## Further Reading

* [contextlib](https://docs.python.org/3/library/contextlib.html) from Python standard library documentation
* [With Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers) from Python standard library documentation
* [Python With Statement](https://realpython.com/python-with-statement) at RealPython
* [Test Doubles](010-dummies-fakes-spies-stubs-mocks.md) article here
