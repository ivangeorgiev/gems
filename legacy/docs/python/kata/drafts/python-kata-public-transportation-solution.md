# Public Transportation - Python Kata Solution

## Solution 1

Your solution might look like the following:

```python
import os

STAGING_DIR = '.'

while True:
    for filename in os.listdir(STAGING_DIR):
        filepath = os.path.join(STAGING_DIR, filename)
        if os.path.isfile(filepath):
           with open(filepath, 'r') as file:
              for line in file:
                 for word in line.split(' '):
                    save_word(word)

```

Although this is not the worst solution I have seen, it has some weaknesses:

* Deep statement nesting at 6 nesting levels. This makes the code very difficult. Where should I add the sleep calls?
* No error handling. If you add try-except blocks, nesting will become even deeper.
* Difficult to test. You might have followed the "growing onion layers" approach which helped in the initial development, but how would you test changes, bug fixes, Python version upgrades?
* Difficult to reuse. Actually templating or as I prefer calling it - copy/paste/edit - is the only way to reuse such a code.

## Solution 2



```python
class WordLoader:
    
    def _get_line_words(self, line):
        return line.split(' ')
            
    def _get_file_lines(file_name):
    	with open(file_name, 'r') as file:
            yield file
    
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

load_file_list = FileLoader()

while True:
    file_list = [f for f in os.listdir(STAGING_DIR) if 
                 os.path.isfile(os.path.join(STAGING_DIR, f))]
    load_file_list(file_list)
      
```



## Solution 3

```python
def repeat(function, before=None, after=None):
    while True:
        try:
            value = function()
        except StopIteration:
            break
        if before is not None:
            before(value)
        yield value
        if after is not None:
            after(value)

def pipeline(iterable, function, before=None, after=None):
    for item in terable:
        if before is not None:
            item = before(item)
        function(item)
        if after is not None:
            after(item)
        
            
def ls_staged_files():
    file_list = [f for f in os.listdir(STAGING_DIR) if \
        os.path.isfile(os.path.join(STAGING_DIR, f))]
    return file_list

def after_file_list(item):
    time.sleep(3)

def get_lines_from_files(files):
    for filename in files:
        filepath = os.path.join(STAGING_DIR, filename)
        with open(filepath, 'r') as file:
            for line in file:
                yield line

def get_words_from_lines(lines):
    for line in lines:
        for word in line.split(' '):
            yield word

def open_files(filenames):
    for filename in filenames:
        filepath = os.path.join(STAGING_DIR, filename)
        with open(filepath, 'r') as file:
            yield file
            
STAGING_DIR = '.'

filelist_sequence = repeat(ls_staged_files, after=after_file_list)
filename_sequence = itertools.chain.from_iterable(filelist_sequence)
file_sequence = open_files(filename_sequence)
file_sequence = itertools.chain.from_iterable(repeat(ls_staged_files, after=after_file_list))
line_sequence = get_lines_from_files(file_sequence)
word_sequence = get_words_from_lines(line_sequence)
for word in word_sequence:
    print(word)
```





