import pandas as pd
import sys
from common import * 
import bs4 
def search_json(search):
    global x
    result = []
    for xx in x:
        for xxx in xx:
            if xx[xxx] == search:
                result.append(xx)
    return result


# def dup_lines(filename):
#     lines = []
#     result = []
#     with open(filename) as f:
#         lines = f.readlines()
#     for line in lines:
#         if lines.count(line) > 1 and line not in result:
#             result.append(line.strip())

#     return result


def dup_lines(filename):
    lines = []
    result = []
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    for line in lines:
        if lines.count(line) > 1 and line not in result:
            result.append(line)
    return result


def get_list(filename):
    return [x.strip() for x in open(filename, "r").readlines()]


def get_csv_col(filename, col_name):
    import csv

    with open(filename, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        col_index = header.index(col_name)
        return [row[col_index] for row in reader]


def not_in_first_list(first_list, second_list):
    return list(set(second_list) - set(first_list))


def not_in_second_list(first_list, second_list):
    return list(set(first_list) - set(second_list))


if __name__ == '__main__':
    if sys.argv[1] == 'get-br_ids':
        year = int(sys.argv[2])
    
    
    