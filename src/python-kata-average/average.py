from collections import namedtuple
import csv
import sys

FILE_NAME = 'techcrunch.csv'
lines = (line for line in csv.reader(open(FILE_NAME)))
# last_line = (s.rstrip().split(',') for s in lines)
last_line = lines
cols = next(last_line)
Row = namedtuple('Row', cols)

# data = (dict(zip(cols,row)) for row in last_line)
data = (Row(*row) for row in last_line)

#size = sys.getsizeof(list(data))
#print(size)

i = 0
for x in data:
    i += 1
    print(i, x)
