Unpacking items from iterables
================================

Packing with * operator
-------------------------

The ``*`` operator extends the unpacking functionality to allow us to collect multiple values into a single variable. Using the ``*`` operator the following example is packing the tuple values into a single variable ``x``:

.. code-block::

   >>> *x, = "a", "b", "c", "d"
   >>> print(x)
   ['a', 'b', 'c', 'd']

For unpacking to work the left side of the assignment needs to be ``tuple`` or ``list`` of variables. For that reason we added the comma after ``x``.

You can specify as many variables in the left side as necessary, but you there could be only one starred variable. The starred variable will receive zero, one or more values from positions that do not match other variables::

   >>> x, *y = "a", "b", "c", "d"
   >>> print(x)
   a
   print(y)
   ['b', 'c', 'd']

First variable ``x`` matches the first item ``a`` on the right side of the assignment. Rest of the items are matched with ``y``.

Starred variable could be in the beginning, end or middle of the tuple::

   x, *y, z = "a", "b", "c", "d"
   >>> print(x)
   a
   >>> print(y)
   ['b', 'c']
   >>> print(z)
   d

Starred variable will be assigned an empty list if no elements on the right side of the assignment are unmatched::

   >>> name, *age = "John".split(",")
   >>> print(name)
   John
   >>> print(age)
   []
