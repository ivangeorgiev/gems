# Test case basics

## Naming test cases

The test case name should start with `test_`. This is a common convention used by test frameworks to discover test cases.

## Test case structure

Test cases usually are executed in three steps Arrange-Act-Assert, also known as Given-When-Then:

1. Arrange\
   In this part, you prepare any objects or values for the test. For example initializing variables, loading data from a file, creating records in the database etc.
2. Act\
   In this part you perform the action that you want to test. Could be call to a function, executing HTTP call to a rest API, interacting with a user interface, etc.
3. Assert\
   In this step you validate that the result from the action matches the expected result. This could involve checking the output of a function, object state, validating expected exception etc.

Example:

```python
def int_addition(x, y):
    return x + y

def test_int_addition():
    # Arrange
    x = 1
    y = 2

    # Act
    actual_result = int_addition(x, y)

    # Assert
    assert actual_result == 3
```
