import csv
import os
import json
import re


def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = csv.DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)


def write_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'w', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = csv.DictWriter(write_obj, fieldnames=field_names)
        dict_writer.writeheader()
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)


def search_csv(file_name, ubit):
    if not os.path.isfile(file_name): return False
    with open(file_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] == ubit:
                return True
    return False


def read_csv(file_name):
    ret = list()
    if not os.path.isfile(file_name): return ret
    with open(file_name, newline='', encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row != None: ret.append(row)

    tmp = list()
    for coord in ret:
        tmp.append([int(coord[0]), int(coord[1])])
    return tmp


def read_json(file_name):
    try:
        with open(file_name) as f:
            data = json.load(f)
    except:
        data = None
    return data


def modify(path):
    if not os.path.isfile(path):
        return

    with open(path) as f:
        lines = f.read().splitlines()

    with open(path, 'w') as f:
        for line in lines:
            # tmp = line.rstrip()
            if re.search("\s+choices=\S+", line):
                f.write(line.replace('choices=', '# choices=') + '\n')
            else:
                f.write(line + '\n')


def checkIfImplemented(path):
    if not os.path.isfile(path):
        return False
    with open(path) as f:
        lines = f.read().splitlines()
    for line in lines:
        line = line.rstrip()

        if re.search("^\s+raise NotImplementedError",line):
            return False
    return True
