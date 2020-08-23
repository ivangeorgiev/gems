# Pipe and Filter in Python

The Pipe and Filter is a very popular architecture style. It can be found in may software development frameworks, like Spark, JavaScript, etc. Linux command line shell also supports piping. You can run one command and direct the output of that command to another command. The output of the second command can be directed to a third command and so on and so forth.

We want to have something similar in Python - piping or chaining together series of transformations on a sequence. Transformations are applied with following patterns:

* `map` - takes as an argument a transformation. When the pipeline is executed, the transformation is applied to each element from the  input and is placed in the output.
* `flat_map` - takes as an argument a transformation. The transformation is expected to produce iterable. When the pipeline is executed, the transformation is applied to each element from the input, each element from the resulting iterable is placed into the output pipeline.

Here is an example what it might look like using the implementation.

**Example:**

* Input: a list of integers [4,6,9]
* Transformation 1: divide each integer by 2 and convert to integer
* Transformation 2: convert each item into a sequence, e.g. 1 becomes [1], 2 becomes [2, 2], 3 becomes [3,3,3], etc. Flatten the result.

*Python code:*

```python
pipe = (Pipe([4,6,9])
        .map(lambda x: x/2)
        .flat_map(lambda x: str(x)*int(x)))
for item in pipe:
    print(item)
```

*Output:*

```
2
2
3
3
3
4
4
4
4
```



 



