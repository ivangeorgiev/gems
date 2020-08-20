---
tags: python, tricks
created: 2020-08-19 08:05:00
---

# Unpacking a Python sequence into variables



## Problem 

You have a list, tuple or another sequence that you want to unpack into a collection of variables.

## Solution

You use assignment operator. On the left side of the operator you define a tuple with the variables. On the right side of the operator is the sequence. The only requirement is that the number of variables and structures match the sequence.

Example:

```python
>>> p = (5, 6)
>>> x, y = p
>>> x
5
>>> y
6

```

Elements of the sequence could be any objects - integer, sequence, etc. Here is an example:

```python
>>> data = [ 'ACME', 50, 91.1, (2012, 12, 21)]
>>> name, shares, price, date = data
>>> name
'ACME'
>>> shares
50
>>> price
91.1
>>> date
(2012, 12, 21)

```

## Discussion

In fact unpacking works with any iterable Python object. This includes strings, files, iterators, and generators.

Sometimes in your assignment, you want to ignore some of the values at certain places from the sequence. Python doesn't have a special syntax for this. Common practice is to use special variable name, e.g. underscore `_`, for places you want to ignore.

```python
>>> data = [ 'ACME', 50, 91.1, (2012, 12, 21)]
>>> name, _, _, date = data
>>> name
'ACME'
>>> date
(2012, 12, 21)

```

