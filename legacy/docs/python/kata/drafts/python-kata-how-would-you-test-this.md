---
tags: python, tdd
categories: python/tdd
---

# Python Kata #?: How would you test this?

You have to implement a function which reads a csv file and returns Python generator of rows. The first line of the csv file is a header.

* Each row is a namedtuple object with named fields according to the header.
* File must be closed after the generator is exhausted or stopped.
* Throws FormatError exception in case of parsing errors.

```python
from collections import namedtuple

def read_csv(file_name):
    with open(file_name) as file:
        lines = (line for line in file)
    data_rows = (row for row in csv.reader(lines))
    header_row = next(data_rows)
    Row = namedtuple('Row', header_row)
    rows = (Row(*row) for row in data_rows)
    return rows

```

