import os
import re
import csv
import json


from Json_Annotator.json_check_annotator import *


def read_json(file_name):
    try:
        with open(file_name) as f:
            data = json.load(f)
    except:
        data = None
    return data


def retrieve_from_json(file_name, image_name):
    out = []

    flag = json_integrity_check(file_name)
    if not flag: return out
    data = read_json(file_name)
    if data is None: return out


    for item in data:
        if item["iname"] == image_name:
            out.append(item["bbox"])

    return out


def concat_list(ls):
    ret = ""

    for i, box in enumerate(ls):
        ret  = ret + "box {}: {}-{}-{}-{}; ".format(i, box[0], box[1], box[2], box[3])

    ret = ret[:200]
    return ret



def json_to_string(json_file, image_name):
    return concat_list(retrieve_from_json(json_file, image_name))



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


def write_to_csv(file_name, dict_of_elem, field_names):
    if os.path.isfile(file_name):
        append_dict_as_row(file_name, dict_of_elem, field_names)
    else:
        write_dict_as_row(file_name, dict_of_elem, field_names)



def get_name(line):
    name = re.findall('_([a-z0-9]+)_attempt*', line)

    retname = name[0]

    return retname


def get_face_py(dir):
    for file in os.listdir(dir):
        if "face" in file.lower():
            return file

    return None


def search_csv(file_name, ubit):
    if not os.path.isfile(file_name): return False
    with open(file_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] == ubit:
                return True
    return False


