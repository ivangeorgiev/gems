---
created: 2020-08-24 20:22:00
tags: python,pipeline
---

# Chain it! Or data pipelining with Python

![pipeline](img/pipeline.jpg)

Recently I worked on a data processing pipeline. A bunch of source systems deliver files into a staging folder. An agent, written in Python, is monitoring the staging folder and is processing all the files from the folder, extracting the words and and loading them into a database. 

We could easily end up with something like:

```python
while True:
    for file_list in ls_files(STAGING_PATH):
        for file_name in itertools.chain.from_iterable(file_list):
            for file in open(os.path.join(STAGING_PATH, fn), file_name):
                for line in file:
                    line_prepared = re_non_alpha_characters.sub(' ', l).lower()
                    words = line_prepared.split(' ')
                    for word in words:
                        save_word(word.strip())
    finish_batch()
```

Nice, isn't?

But - not easy to read and understand. How about testing?

Where and how should I add exception handling? What about files - who is going to close them and when? How I can add new functionality, e.g. extract text from PDF files or images or automatic language translation? How we could accommodate business logic - e.g. search for similar words with Levenshtein distance, bucket words in categories, etc. How could multiple developers work on this solution? Well ... This one is easy and quick to start, but quickly becomes messy.

To address these concerns I was aiming at expressive, flexible, testable and extensible code.

First thing was to refactor the code in a way to remove the nesting of the statements. The `main()` function of the agent looks now very simple:

```python
def main():
    for word in build_word_pipeline():
        save_word(word)
```

 The `build_word_pipeline()` function is:

```python
def build_word_pipeline():
	batch_source = after_it(finish_batch, repeater(get_batch))
    file_names = flat_map(None, batch_source)
    file_names_with_path = map(lambda fn: os.path.join(STAGING_PATH, fn), file_names)
    lines = flat_map(get_file_lines, file_names_with_path)
    words = flat_map(lambda l: re_non_alpha_characters.sub(' ', l).lower().split(' '), lines)
    words = filter(lambda w: len(w) > 0, words)
    words = map(lambda w: w.lower().strip(), words)
    return words
```

A few words about the functions used in this snippet:

* `repeater` converts a function result into a collection by calling the function repeatedly.
* `after_it` decorates a collection so that a given function (`after_batch`) is called each time after an item from the input collection is consumed.
* `finish_batch` performs a clean up operations and is suspending the execution for a given duration in seconds.
* `flat_map` applies a collection returning mapper function to input collection and is flattening the result by placing each item from the result collections into the output.
* `filter` is a standard Python function for filtering a collection.
* `map` is a standard Python function for applying a function to each element from a collection. 
* `re_non_alpha_characters` is a regular expression for finding non alpha characters.

All above functions are lazy and work through Python generators and iterators.

And I can easily write unit tests for this code.

Looking at the result code, I was thinking - how I can make it more readable and easy to understand?

First thing would be to convert lambdas to regular functions with meaningful names.

```python
def build_word_pipeline():
    batch_sorce = repeater(get_batch)
	batches_with_after = after_it(finish_batch, batch_sorce)
    file_names = flat_map(None, batch_source)
    file_names_with_path = map(make_path, file_names)
    lines = flat_map(get_file_lines, file_names_with_path)
    words = flat_map(split_into_words, lines)
    words = filter(None, words)
```

I think it is better now. I have to issues with this:

* I find it difficult to name all the intermediate steps
* There is a lot of repetition. The collection variable from the previous line is used as argument in the next line. This is like moving water with buckets - Fill the bucket at left side, bring it to the right side, empty it in the processing unit and go back to the right with the empty bucket for the next task.

Could we address these two issues? What I was looking for is:

<script src="https://gist.github.com/ivangeorgiev/b5b187432359384cb9f1eb8d4df4509e.js"></script>

The solution is in the decorator pattern. We start with a collection wrapped into a decorator `Pipe`. Than we apply a transformation which returns another `Pipe` decorator which bundles also the transformation. And we continue until we get all the processing we need defined.

Here is the source for the `Pipe` class:

<script src="https://gist.github.com/ivangeorgiev/a6b3d6dc458391a38e693af7aba7a99c.js"></script>

In the implementation there is one addition - the `before`  method which calls a function before the next item from the collection is returned. The same effect could be achieved using `map`, but I added it for symmetry with `after` method and as syntactic sugar.

Think about following. Using the Pipe approach, can you make the solution configuration driven? Can you turn on or off stages, using feature flags?

