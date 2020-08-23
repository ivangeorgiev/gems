---
created: 2020-08-22 17:27:30
tags: python,tdd,kata
---

# Python Kata #1: Pipe and Filter

The Pipe and Filter is a very popular architecture style. It can be found in may software development frameworks, like Spark, JavaScript, etc. Linux command line shell also supports piping. You can run one command and direct the output of that command to another command. The output of the second command can be directed to a third command and so on and so forth.

We want to have something similar in Python - piping or chaining together series of transformations on a sequence. Transformations are applied with following patterns:

* `map` - takes as an argument a transformation. When the pipeline is executed, the transformation is applied to each element from the  input and is placed in the output.
* `flat_map` - takes as an argument a transformation. The transformation is expected to produce iterable. When the pipeline is executed, the transformation is applied to each element from the input, each element from the resulting iterable is placed into the output pipeline.
* `filter` - takes as an argument a bool function. Function is applied for each element in the input. If the filter function returns true, the element is placed in the output. Otherwise the element is dropped.

To implement these patterns you might find useful the Python functions `map`, `filter`, `reduce (See [Map, Filter and Reduce](https://book.pythontips.com/en/latest/map_filter.html) at Intermediate Python)

Do not forget to test your solution!

Here is an example what it might look like using the implementation.

**Example:**

* *Input:* a list of strings, e.g. ['Lorem ipsum', 'dolorem costum']
* *Transformation 1:* convert all items to lower case, e.g. ['lorem ipsum', 'dolorem costum']
* *Transformation 2:* split each element into, e.g. ['lorem', 'ipsum', 'dolorem', 'costum']
* *Transformation 3:* remove all words ending with 'em', e.g. ['ipsum', 'costum']

*Python code:*

```python
pipe = (Pipe(['Lorem ipsum', 'dolorem costum'])
        .map(lambda x: x.lower())
        .flat_map(lambda x: x.split(' '))
        .filter(lambda x: not x.endswith('em')))
for item in pipe:
    print(item)
```

*Output:*

```
ipsum
costum
```



 



