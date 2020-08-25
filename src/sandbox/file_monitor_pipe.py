import sys, os
import time
import logging
import itertools
import re

# lib_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'python-iterator-repeater')
# sys.path.append(lib_path)

STAGING_PATH = '.'
FILE_LIST_SLEEP_INTERVAL = 5
LOG_LEVEL = 'DEBUG'

logging.basicConfig(level=LOG_LEVEL)

class Pipe:
    def __init__(self, seq):
        self._seq = seq

    def __iter__(self):
        return iter(self._seq)
    
    def map(self, func):
        return Pipe(map(func, self))

    def flat_map(self, func=None):
        maped_iter = self if func is None else map(func, self)
        return Pipe(itertools.chain.from_iterable(maped_iter))

    def filter(self, func=None):
        return Pipe(filter(func, self))
    
    def before(self, func):
        return Pipe(before_it(func, self))

    def after(self, func):
        return Pipe(after_it(func, self))


def repeat(value):
    value = value if callable else lambda: value
    while True:
        yield value()

def before_it(func, iter1):
    for it in iter1:
        func()
        yield it

def after_it(func, iter1):
    for it in iter1:
        yield it
        func()

def ls_files(path):
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            yield entry

def get_batch():
    return ls_files(STAGING_PATH)

def after_batch():
    logging.info(f'Sleeping for {FILE_LIST_SLEEP_INTERVAL} seconds')
    time.sleep(FILE_LIST_SLEEP_INTERVAL)

def get_file_lines(file_name):
    with open(file_name) as file:
        for line in file:
            yield line

re_non_alpha_characters = re.compile('[^a-zA-Z]')

words = (Pipe(repeat(get_batch))
             .after(after_batch)
             .flat_map(lambda x:x)
             .map(lambda fn: os.path.join(STAGING_PATH, fn))
             .flat_map(get_file_lines)
             .flat_map(lambda line: re_non_alpha_characters.sub(' ', line).lower().split(' '))
             .filter())


for entry in words:
    print(entry)
