# Parameterize Unittest Tests

Python unittest package is part of Python standard library. It is very handy and powerful tool for creating, discovering and executing unit tests for Python code.

However unittest doesn't provide a way to parameterize the tests. With test parameterization the same test is executed multiple times with different arguments passed. Using this approach we avoid repetition and in most cases tests are easier to read and more expressive.

## `parameterized` Package

The [parameterized](https://github.com/wolever/parameterized) brings tools which allow to parameterize tests for pytest, unittest, nose and other Python testing frameworks.

## Our kata

To learn how to parameterize tests in Python we will use a real problem, such problems, executed as learning process are known as kata. In this kata we are asked to find the smallest window in array which needs to be sorted in order to sort the whole array:

> Given an array of integers that are out of order, determine the bounds of the smallest
> window that must be sorted in order for the entire array to be sorted. For example,
> given [ 3 , 7 , 5 , 6 , 9] , you should return ( 1 , 3 ) .

Here is one possible solution in Python of our smallest sort window kata:

```python
def smallest_window_to_sort(nums):
    left, right = None, None
    max_seen, min_seen = -float("inf"), float("inf")
    n = len(nums)

    for i in range(n):
        if max_seen < nums[i]:
            max_seen = nums[i]
        if nums[i] < max_seen:
            right = i

    for i in range(n-1, -1, -1):
        if min_seen > nums[i]:
            min_seen = nums[i]
        if nums[i] > min_seen:
            left = i

    return left, right
```

I am not going in details how to solution works. Our goal is to verify it works correctly.

### Smallest sort window kata tests

We could define following tests to verify that our solution works correctly:

| test # | name | input | expected result |
|:-:|------|-------|-----------------|
| 1|empty array| `[]`| `(None, None)` |
| 2|array with one element | `[10]` | `(None, None)` |
| 3|already sorted array | `[1, 2, 3, 4, 5]` | `(None, None)`|
| 4|reverse sorted array | `[5, 4, 3, 2, 1]` | `(0, 4)`|
| 5|array with same element | `[7, 7, 7, 7, 7, 7]` | `(None, None)` |
| 6|array with two elements in the middle out of order | `[1, 2, 4, 3, 5]` | `(2, 3)` |
| 7|array with elements out of order at the beginning | `[2, 1, 3, 4, 5]` | `(0, 1)` |
| 8|array with repeated elements | `[1, 5, 5, 4, 3, 3, 6]` | `(1, 5)`  |

## Parameterize Unittest Test

Looking at the defintions of our tests, all they are exercising the output of the function, given some input. In other words they assert that the output produced by the function matches the expectation for the given input.

Implemented as Python's unittest test case, our test would look like following.

```python
import unittest

class TestSmallestWindowToSortFunction(unittest.TestCase):
    def test_it(self, input, expected_result):
        actual_result = smallest_window_to_sort(input)
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored', '-v'], exit=False)
```

Looks pretty neat, ah? The only problem is that this is not a valid test as there is no way to tell unittest that we want this test case to be executed multiple times, passing the arguments from our test defintion table.

Trying to execute the test case will result in error:

```bash
$ python smallest_window_to_sort/smallest_window_to_sort.py
```
```
test_it (__main__.TestSmallestWindowToSortFunction) ... ERROR

======================================================================
ERROR: test_it (__main__.TestSmallestWindowToSortFunction)
----------------------------------------------------------------------
TypeError: TestSmallestWindowToSortFunction.test_it() missing 3 required positional arguments: 'name', 'input', and 'expected'

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
```

Here comes the `parameterized` package. We are using the `@parameterized.expand` decorator.

The deocrator takes as an argument a list of tests scenarios to be executed for the same test. Each element in the list is a tuple, defining a test scenario. All the elements of the tuple are passed as arguments to the test. The first element is the name of the scenario.

```python
import unittest
from parameterized import parameterized, parameterized_class

def smallest_window_to_sort(nums):
    left, right = None, None
    max_seen, min_seen = -float("inf"), float("inf")
    n = len(nums)

    for i in range(n):
        if max_seen < nums[i]:
            max_seen = nums[i]
        if nums[i] < max_seen:
            right = i

    for i in range(n-1, -1, -1):
        if min_seen > nums[i]:
            min_seen = nums[i]
        if nums[i] > min_seen:
            left = i

    return left, right

class TestSmallestWindowToSortFunction(unittest.TestCase):
    @parameterized.expand([
        ("empty_array", [], (None, None)),
        ("array_with_one_element", [10], (None, None)),
        ("already_sorted_array", [1, 2, 3, 4, 5], (None, None)),
        ("reverse_sorted_array", [5, 4, 3, 2, 1], (0, 4)),
        ("array_with_repeated_element", [7, 7, 7, 7, 7, 7], (None, None)),
        ("arrawy_with_two_elements_in_middle_out_of_order", [1, 2, 4, 3, 5], (2, 3)),
        ("arrawy_with_elements_out_of_order_at_beginning", [2, 1, 3, 4, 5], (0, 1)),
        ("arrawy_with_repeated_elements_out_of_order", [1, 5, 5, 4, 3, 3, 6], (1, 5)),
    ])
    def test_it(self, name, input, expected):
        result = smallest_window_to_sort(input)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored', '-v'], exit=False)
```

Now the test is executed as expected:

```
test_it_0_empty_array (__main__.TestSmallestWindowToSortFunction) ... ok
test_it_1_array_with_one_element (__main__.TestSmallestWindowToSortFunction) ... ok
test_it_2_already_sorted_array (__main__.TestSmallestWindowToSortFunction) ... ok
test_it_3_reverse_sorted_array (__main__.TestSmallestWindowToSortFunction) ... ok
test_it_4_array_with_repeated_element (__main__.TestSmallestWindowToSortFunction) ... ok
test_it_5_arrawy_with_two_elements_in_middle_out_of_order (__main__.TestSmallestWindowToSortFunction) ... ok
test_it_6_arrawy_with_elements_out_of_order_at_beginning (__main__.TestSmallestWindowToSortFunction) ... ok
test_it_7_arrawy_with_repeated_elements_out_of_order (__main__.TestSmallestWindowToSortFunction) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.003s

OK
```

## Under the hood

Looking at the output from unittest execution of our parameterized Python test, you might have already guessed how the `@parameterized.expand` decorator works.

For each test, defined, the decorator creates a new test method, adding a sequential number to the new method's name and the name from the test defintion.

## Going beyond - parameterizing algorithms

Along with parameterization of tests, the `parameterized` package allows for parameterization of test cases. It works the same way as parameterizatoin of tests, but creates a new test case (test class) for each scenario.

Let's assume we have created another solution of the problem which we want to test, using the same tests.

```python
def smallest_window_to_sort_with_sorted(nums):
    left, right = None, None
    s = sorted(nums)

    for i in range(len(nums)):
        if nums[i] != s[i] and left is None:
            left = i
        elif nums[i] != s[i]:
            right = i
    return (left, right)
```

We could use the `@parameterized_class` decorator from the `parameterized` package to create multiple test cases for both algorithms.

The form we are using takes two arguments.
1. List of class attributes to be set for each test case generated.
2. List of tuples defining the test scenarios. Each tuple specifies the values to be assigned to the class attributes for the test case generated for the test scenario.

We want to have two test scenarios for each algorithm we want to exercise. The algortihm being exercised is set as `function_to_test` class attribute.

```python
@parameterized_class(("function_to_test",),
                     [
                        (staticmethod(smallest_window_to_sort), ),
                        (staticmethod(smallest_window_to_sort_with_sorted), ),
                     ])
class TestSmallestWindowToSortFunction(unittest.TestCase):
    @parameterized.expand([
        ("empty_array", [], (None, None)),
        ("array_with_one_element", [10], (None, None)),
        ("already_sorted_array", [1, 2, 3, 4, 5], (None, None)),
        ("reverse_sorted_array", [5, 4, 3, 2, 1], (0, 4)),
        ("array_with_repeated_element", [7, 7, 7, 7, 7, 7], (None, None)),
        ("arrawy_with_two_elements_in_middle_out_of_order", [1, 2, 4, 3, 5], (2, 3)),
        ("arrawy_with_elements_out_of_order_at_beginning", [2, 1, 3, 4, 5], (0, 1)),
        ("arrawy_with_repeated_elements_out_of_order", [1, 5, 5, 4, 3, 3, 6], (1, 5)),
    ])
    def test_it(self, name, input, expected):
        func = self.function_to_test
        result = func(input)
        self.assertEqual(result, expected)
```

The result of the test execution is as follows:

```
test_it_0_empty_array (__main__.TestSmallestWindowToSortFunction_0) ... ok
test_it_1_array_with_one_element (__main__.TestSmallestWindowToSortFunction_0) ... ok
test_it_2_already_sorted_array (__main__.TestSmallestWindowToSortFunction_0) ... ok
test_it_3_reverse_sorted_array (__main__.TestSmallestWindowToSortFunction_0) ... ok
test_it_4_array_with_repeated_element (__main__.TestSmallestWindowToSortFunction_0) ... ok
test_it_5_arrawy_with_two_elements_in_middle_out_of_order (__main__.TestSmallestWindowToSortFunction_0) ... ok
test_it_6_arrawy_with_elements_out_of_order_at_beginning (__main__.TestSmallestWindowToSortFunction_0) ... ok
test_it_7_arrawy_with_repeated_elements_out_of_order (__main__.TestSmallestWindowToSortFunction_0) ... ok
test_it_0_empty_array (__main__.TestSmallestWindowToSortFunction_1) ... ok
test_it_1_array_with_one_element (__main__.TestSmallestWindowToSortFunction_1) ... ok
test_it_2_already_sorted_array (__main__.TestSmallestWindowToSortFunction_1) ... ok
test_it_3_reverse_sorted_array (__main__.TestSmallestWindowToSortFunction_1) ... ok
test_it_4_array_with_repeated_element (__main__.TestSmallestWindowToSortFunction_1) ... ok
test_it_5_arrawy_with_two_elements_in_middle_out_of_order (__main__.TestSmallestWindowToSortFunction_1) ... ok
test_it_6_arrawy_with_elements_out_of_order_at_beginning (__main__.TestSmallestWindowToSortFunction_1) ... ok
test_it_7_arrawy_with_repeated_elements_out_of_order (__main__.TestSmallestWindowToSortFunction_1) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.005s

OK
```

As you could see, the `@parameterized_class` decorator creates a new test class for each scenario defined by the decorator arguments. Each class has attributes set to the values specified for the corresponding test. In our case:

| test case | `function_to_test` attribute |
|-----------|------------------------------|
| TestSmallestWindowToSortFunction_0 | `smallest_window_to_sort`|
| TestSmallestWindowToSortFunction_1 | `smallest_window_to_sort_with_sorted`|

## Conclusion

The `parameterized` package provides handy tools to avoid duplications in python's tests and make our tests much more expressive. Pytest already provides tools for test parameterization, but `unittest` is missing them.

To get more of the `parameterized` package, it is recommended that you look at the [documentation](https://github.com/wolever/parameterized). For example, it is possible to pass values to keyword arguments, using `param`, use custom function for naming tests, etc.
