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

def ls_staged_files():
    file_list = [f for f in os.listdir(STAGING_DIR) if \
        os.path.isfile(os.path.join(STAGING_DIR, f))]
    return file_list

def after_file_list(item):
    time.sleep(3)

def get_file_lines(filename):
    with open(os.path.join(STAGING_DIR, filename), 'r') as file:
        for line in file:
            yield line

STAGING_DIR = '.'

for file_list in repeat(ls_staged_files, after=after_file_list):
    for filename in file_list:
        for line in get_file_lines(filename):
            for word in line.split(' '):
                print(word)



def get_words_from_lines(lines):
    for line in lines:
        for word in line.split(' '):
            yield word

####################################################################################

import os
import itertools
import time
import logging

def iter_call(function, before=None, after=None):
    """Return results from iterative calls to a function until StopIteration is raised."""
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

def ls_files(dir):
    file_list = [f for f in os.listdir(dir) if \
        os.path.isfile(os.path.join(dir, f))]
    return file_list

def list_filename_lists():
    for filename_lists in iter_call(lambda: ls_files(STAGING_DIR)):
        logging.info(f'Received {len(filename_lists)} files')
        yield filename_lists
        logging.info('Sleeping for 3 seconds')
        time.sleep(3)

def list_files(filename_lists):
    for filename in itertools.chain.from_iterable(filename_lists):
        logging.info(f"Begin processing file '{filename}'")
        filepath = os.path.join(STAGING_DIR, filename)
        try:
            with open(filepath, 'r') as file:
                yield file
            logging.info(f"End processing file '{filename}'")
        except:
            logging.error(f"Error processing file '{filename}'", exc_info=True)

def list_lines(files):
    return itertools.chain.from_iterable(files)

def list_words(lines):
    for line in lines:
        for word in line.split(' '):
            yield word

def save_word(word):
    log.debug(f"saving word '{word}'...")

STAGING_DIR = '.'


logging.basicConfig(level=logging.INFO)

filename_lists = list_filename_lists() # [ls_files(STAGING_DIR)] # repeat(ls_staged_files, after=after_file_list)
files = list_files(filename_lists)
lines = list_lines(files)
words = list_words(lines)
for word in words:
    pass
    save_word(word)


class Pipe:
    def __init__(self, seq):
        self._sequence = seq

    def __iter__(self):
        return iter(self._sequence)

class Repeater:
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return self

p = Pipe([1,2,3])


pipe(source)
   .map(func)
   .flat_map(func)
   .map(save)





