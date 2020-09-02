---
tags: python, design patterns, singleton
created: 2020-09-02 15:00:00
---

# Convert a Python class to Singleton using decorator

In Python there are many ways to implement the [Singleton Pattern](https://en.wikipedia.org/wiki/Singleton_pattern). For example:

* Modules are singletons in Python.
* You could use java-like implementation, combined with factory method. 

There is another interesting pythonic way to turn any class into a singleton. You could use a Python decorator and apply it to the class you want to be a singleton.

Probably more pythonic would be to use a meta class to create a singleton. This is another story. I will tell you this story soon. 

## Python Singleton Decorator

The decorator is changing the way new objects are created from the decorated class. Each time you are requesting a new object, you will get the same object again and again.

Here is the definition of the singleton decorator:

```python
from functools import wraps

def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls, *args, **kwargs)
        return instance
    orig_cls.__new__ = __new__
    return orig_cls
```

Here is an example usage:

```python
@singleton
class Logger:
    def log(msg):
        print(msg)

logger1 = Logger()
logger2 = Logger()
assert logger1 is logger2
```

In this example we have a simple `Logger` class with a single method `log` which logs a message. For simplicity our implementation is just printing the message to the standard output.

We are creating two `Logger`  objects - `logger1` and `logger2`  we verify that the two variables are actually referring to the same object, using the `assert` statement.

## Try it out

Here is a [Jupyter notebook I created as GitHub gist](https://gist.github.com/ivangeorgiev/d4bd94bc69f14fe35324f4855a4db9f1). You can use this notebook to try the above example.

<script src="https://gist.github.com/ivangeorgiev/d4bd94bc69f14fe35324f4855a4db9f1.js"></script>

## How the singleton decorator works? 

This solution is based on the way Python creates new instances of a class. When a new instance is to be created, the special method of the class, called `__new__`, is called to create the instance. The method should return the newly created instance. In this solution the decorator is overwriting the original `__new__` method of the class so that it will return same instance each time it is called.

When you add a decorator to a class, the decorator function is called once, receiving as a first argument the decorated class. The decorator stores a reference to the original `__new__` method of the decorated class into a variable named`orig_new`, the original `__new__` method is replaced with different implementation.

The new implementation of the `__new__` method is checking if an instance of the class has already been created. If this is the first call to the function the `instance` variable is not set. The original method referenced by the `orig_new` variable is called to create the initial instance of the class. The object is stored in in the `instance` variable and is returned as a result from the function.

Further calls to the function will not create new instances, but will directly return the initial instance, stored in the `instance` variable.

## Discussion

A little bit more advanced implementation of the Singleton pattern would be to have named object instances. For example, you might want to have different loggers. For example:

* `Logger('database')` returns an instance for logging database messages.
* `Logger('http')` returns an instance for logging HTTP requests.

## Further Reading

* You can learn more about the way the `__new__` method works in the [Python documentation](https://docs.python.org/3/reference/datamodel.html#object.__new__).