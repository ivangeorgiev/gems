import csv
from collections import namedtuple

def get_file_lines(file_name):
    global file
    with open(file_name) as file:
        return (line for line in file)

def read_csv(file_name):
    lines = get_file_lines(file_name)
    data_rows = (row for row in csv.reader(lines))
    header_row = next(data_rows)
    Row = namedtuple('Row', header_row)
    rows = (Row(*row) for row in data_rows)
    return rows
