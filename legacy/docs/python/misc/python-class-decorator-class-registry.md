# Python Class Decorator Primer - Class Instance Registry

Let's assume we have a situation where we need to keep track about eache instance of a class.

The source code used in this document could be found on github [registered class decorator](https://gist.github.com/ivangeorgiev/204c8e0310c2a7eea07970eae824f3a1).

This could be illustrated using following snippet:

```python
orders = []

@registered(orders)
class Order:
    ...

order1 = Order()
assert order1 in orders
```

Possible implementation for the `registered` decorator might be:

```python
def registered(registry):
    def decorator(cls): # <2>
        def cls_factory(*args, **kwargs):
            instance = cls(*args, **kwargs)
            registry.append(instance)
            return instance

        return cls_factory  # <3>

    return decorator  # <1> 
```

1. Parameterized decorator is a function which is called with the argument passed to the decorator. The function usually returns a decorator.
2. The decorator function is called with decorated class passed as argument.
3. The decorator function returns factory function which will create instances from the decorated class and register them with the provided registry.

Following `pytest` unittests could be used to test the decorator.

```python
import pytest


class FakeClass:
    pass


class TestRegisteredDecorator:
    @pytest.fixture(name="registry")
    def given_registry(self):
        return []

    @pytest.fixture(name="decorated")
    def given_decorated(self, registry):
        return registered(registry)(FakeClass)

    def test_given_decorated_class_when_create_instance_then_instance_is_in_registry(
        self, registry, decorated
    ):
        instance = decorated()
        assert isinstance(instance, FakeClass)
        assert instance in registry
```
