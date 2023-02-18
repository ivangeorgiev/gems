# Iterate over hierarchical sources in Python

## Problem

We are given a list of files and we need to insert the words from files into a database. The sequence of the words should be preserved. 

Here is one way to achieve this:

```python
file_list = ['a.txt', 'b.txt']
for file_name in file_list:
    with open(file_name, 'r') as file:
        for line in file:
            for word in line.split(' '):
                with db.connection.cursor() as cursor:
                    cursor.execute('INSERT INTO words(word) VALUES (?)', (word,))
                    cursor.commit()
```

How do you test such code? Maybe you use something I call 'evolutionary testing' - you start with the outer loop. Add a print statement, run a few times, comment the print statement. And you continue until it is done.

Ok. This might work at the beginning. But how you test your code continuously? There are situations where you need to verify the code is working correctly. For example:

1. New requirements - e.g. process PDF, image files etc.
2. Dependency upgrade - e.g. changing to a higher version of Python
3. Change the target database
4. Issue fixing
5. Error handling

This code is already difficult to read and understand.

You want to improve your code - make it testable, more readable and maintainable, more flexible and extensible.

## Discussion

Look at the code. Isn't it doing too much things? 

## Solution

Let's start with the responsibilities. 

- Iterate over a list of files
- Process a file - iterate over the lines from a file
- Get the lines from a file
- Process a line - iterate over the words in a line
- Get the words from a line
- Process a word - save a word into the database

So we might come with an object-oriented solution like this:

```python
class WordLoader:
    
    def _get_line_words(self, line):
        return line.split(' ')
            
    def _get_file_lines(file_name):
    	with open(file_name, 'r') as file:
            return f
    
    def _process_word(self, word):
        with db.connection.cursor() as cursor:
            cursor.execute('INSERT INTO words(word) VALUES (?)', (word,))
            cursor.commit()        

    def _process_line(self, line):
        for word in self._get_line_words(line):
            self._process_word(word)
    
    def _process_file(self, file_name):
        for line in self._get_file_lines(file_name):
            self._process_line(line)
    
    def __call__(self, file_list):
        for file_name in file_list:
            self._process_file(file_name)
```

Looks much better now. We can test each method in isolation with unit tests.

However I still have some concerns.

The *WordLoader* class we created takes too much responsibilities.

What is going on is still not very visible. To understand what is going on, I need to dig into the whole chain of execution. Can I make my code more expressive so that I can read the code from the very beginning like this: "Insert all the words from a list of files into the database."  Maybe my main code could look like this?

```python
for word in words_from_files:
    save_word(word)
```

Where the `words_from_files`  comes from?

```python
files = get_files_from_name_list(file_list)
lines_from_files = get_lines_from_files(files)
words_from_files = get_words_from_lines(lines_from_files)
```

Wait! You are going to load all these terabytes and petabytes into the memory?

Good point. Not necessarily. Instead of returning list, I could use generators.

```python
def get_files_from_name_list(filename_list):
    for filename in filename_list:
        with open(filename, 'r') as file:
            yield file
            
def get_lines_from_files(files):
    for file in files:
        for line in file:
            yield file

def get_words_from_lines(lines):
    for line in lines:
        for word in line.split(' ')
        	yield word
```

The code is much more expressive now. There are two things I do not like:

* functions look almost the same
* functions are doing more than one thing. Let's take `get_lines_from_files` as an example. It iterates over the files in a list, unpacks the file into lines, using `split()` method and iterates over the resulting words.  

```python
def unpack_containers(containers, unpack):
    for container in containers:
        for item in unpack(container):
            yield item
```

```python
def unpack_filename(filename):
    with open(filename, 'r') as f:
        yield [f]

def unpack_file_lines(file):
    return file

def unpack_line_words(line):
    for word in line.split(' '):
        yeild word

files = unpack_containers(file_list, lambda filename: [open(filename, 'r')])
lines_from_files = get_lines_from_files(files)
words_from_files = get_words_from_lines(lines_from_files)
```





```python
files = map(open_file, file_list)
lines = chain.from_iterable(files)
words = chain.from_iterable(map(lambda line: line.split(' '), lines))

```



```python
def open_file(filename):
    with open(filename, 'r') as f:
        yield f

def get_words_from_line(line):
    return line.split(' ')

def flat_map(function, iterable, *arg):
    arg.insert(0, iterable)
    chain.from_iterable(map(function, *arg))
  
lines = map(open_file, file_list)
words = flat_map(get_words_from_line, lines)
```



```python
def list_new_events():
    with db.cursor() as c:
        c.execute("SELECT * FROM events WHERE status='N'")
        yield c.fetchall()

def repeat(function, before=None, after=None):
    while True:
        if before is not None:
            before()
        yield function()
        if after is not None:
            after()

def reset_process():
    pass

def process(event):
    pass

event_stream = chain.from_iterable(repeat, after=reset_process)
for event in event_stream:
    process(event)

```

