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

def repeater(value):
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

def flat_map(func, it):
    return itertools.chain.from_iterable(map(func, it))

p = re.compile('[^a-zA-Z]')


batch_source = after_it(after_batch, repeater(get_batch))
file_names = flat_map(lambda x:x, batch_source)
file_names_with_path = map(lambda fn: os.path.join(STAGING_PATH, fn), file_names)
lines = flat_map(get_file_lines, file_names_with_path)
words = flat_map(lambda l: p.sub(' ', l).split(' '), lines)
words = filter(lambda w: len(w) > 0, words)
words = filter(lambda w: w.lower().strip(), words)

for entry in words:
    print(entry)
