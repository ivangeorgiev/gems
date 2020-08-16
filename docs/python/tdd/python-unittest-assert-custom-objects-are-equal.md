---
tags: python, tdd
date: 2020-04-16 08:56:00
---

# Assert custom objects are equal in Python unit test

## Problem

You are creating a Python unit test, using `unittest`. Your test needs to assert that two custom objects are equal. For example, you might have following `User` class defined:

```python
class User:
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name
```

Trying to compare two `User` objects for equality, using `assertEqual` fails:

```
>>> import unittest
>>> test_case = unittest.TestCase()
>>> expected = User(1, 'John')
>>> actual = User(1, 'John')
test_case.assertEqual(expected, actual)
Traceback (most recent call last):
...
AssertionError: <__main__.User object at 0x000002BC202AD888> != <__main__.User object at 0x000002BC2000B348>
>>>
```

## Solution

I will present you 3 different solutions to the problem.

* Implement equality interface
* Use `addTypeEqualityFunc`
* Use matcher

Each solution is applicable to different situations.

### Implement equality interface

Because `unittest`  will try to perform Python's equality operator on your `User` objects, if the `User` class implements the equality operator interface, the equality assertion will work. The equality operator interface requires that the class implements a `__eq__` method.

```python
class User:
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id and \
               self.name == other.name
```

Now it is ok to use `assertEqual` :

```
>>> import unittest
>>> test_case = unittest.TestCase()
>>> expected = User(1, 'John')
>>> actual = User(1, 'John')
>>> test_case.assertEqual(expected, actual)
```

`assertNotEqual` also works fine:

```
>>> import unittest
>>> test_case = unittest.TestCase()
>>> expected = User(1, 'John')
>>> actual = User(1, 'Jane')
>>> test_case.assertNotEqual(expected, actual)
```

Using this approach solves our problem, but it has some limitations:

* We need to modify the User class source
* There is no way to have different equality assertions for different situations. For example, we might have situations where equality doesn't include the `id` attribute.

### Use `addTypeEqualityFunc` method

Unittest `TestCase` class provides convenient way to override default Python equality operator by using the `addTypeEqualityFunc`:

```
>>> import unittest
>>> test_case = unittest.TestCase()
>>> test_case.addTypeEqualityFunc(User, lambda first, second, msg: first.name == second.name )
>>> expected = User(1, 'John')
actual = User(2, 'John')
>>> test_case.assertEqual(expected, actual)
```

The limitations of this approach:

* We have to use the same comparison function for a given type in all tests. For example, we might have tests where equality check requires `id` fields to be equal and other tests where `id` fields should not be compared.
* Both parameters to `assertEqual` have to be objects of the same type.

### Use matcher

Another approach would be to create custom matcher object. 

```python
class UserMatcher:
    expected: User

    def __init__(self, expected):
        self.expected = expected

    def __eq__(self, other):
        return self.expected.id == other.id and \
               self.expected.name == other.name
```

Custom matcher could be any class that implements the equality operator. In other words, having the `__eq__`  method implemented.

```
>>> test_case = unittest.TestCase()
>>> expected = User(1, 'John')
>>> actual = User(1, 'John')
>>> test_case.assertEqual(UserMatcher(expected), actual)
```

Although this is the most flexible approach, it is more verbose.

## Discussion

In case of equality assertion fails, the output is not very useful:

```
>>> test_case.assertEqual(UserMatcher(expected), actual)
Traceback (most recent call last):
...
AssertionError: <__main__.UserMatcher object at 0x000002BC20309BC8> != <__main__.User object at 0x000002BC20314388>
```

You could improve this by implementing a `__repr__` method of your custom class:

```python
class User:
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"User(id={repr(self.id)}, name={repr(self.name)})"
```

In case you are using matcher, the matcher should also implement the `__repr__` method:

```python
class UserMatcher:
    expected: User

    def __init__(self, expected):
        self.expected = expected

    def __repr__(self):
        return repr(self.expected)

    def __eq__(self, other):
        return self.expected.id == other.id and \
               self.expected.name == other.name
```

Now we will get much more readable and meaningful assertion failure message:

```
>>> test_case.assertEqual(UserMatcher(expected), actual)
...
AssertionError: User(id=1, name='John') != User(id=2, name='John')
```

