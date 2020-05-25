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


def write_out_csv(file_name, dict_of_elem, field_names):
    if os.path.isfile(file_name):
        append_dict_as_row(file_name, dict_of_elem, field_names)
    else:
        write_dict_as_row(file_name, dict_of_elem, field_names)



