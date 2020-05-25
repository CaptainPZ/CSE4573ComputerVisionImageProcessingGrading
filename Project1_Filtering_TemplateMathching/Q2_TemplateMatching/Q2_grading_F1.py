import argparse
import shlex
import subprocess
from scipy import signal
import sys

import backcall
import copy
import os

import cv2
import numpy as np
import re
import shutil
import zipfile
from csvwriter import append_dict_as_row
from csvwriter import write_dict_as_row
from csvwriter import search_csv
from csvwriter import read_csv
from csvwriter import read_json


def f1_score(groundtruth_ls, input_ls, tp_h, tp_w, tolerance=3.0):
    '''
    :param groundtruth_ls: ls of ls, the ground truth ls
    :param input_ls: ls of ls, the ls from student
    :param tp_h: template height, or # of rows
    :param tp_w: template width, or # of columns
    :param tolerance: the allowed tolerance in radius
    :return: F1 score
    '''

    # check if any input
    if len(input_ls) == 0 :
        return -1

    tp_dict = dict()
    for coord_input in input_ls:
        for coord_ground in groundtruth_ls:
            # print(coord_input)
            if distance(coord_ground[0], coord_ground[1],
                        int(coord_input[0]) + 0.5 * int(tp_h), int(coord_input[1]) + 0.5 * int(tp_w)) < tolerance:
                tp_dict[(coord_ground[0], coord_ground[1])] = 1
                break

    tp = len(tp_dict)
    fp = len(input_ls) - tp
    fn = len(groundtruth_ls) - tp

    if tp == 0: return 0
    precision = (1.0 * tp / (tp + fp))
    recall = (1.0 * tp / (tp + fn))

    f1 = 2.0 * precision * recall / (precision + recall)
    return f1


def distance(x1, y1, x2, y2):
    return ((1.0 * x1 - x2) ** 2 + (1.0 * y1 - y2) ** 2) ** 0.5


def question2_grader(groundtruth_path, json_path):
    if not os.path.isfile(json_path):
        return -1
    gorundtruth_ls = read_csv(groundtruth_path)
    json_file = read_json(json_path)
    if json_file is None: return -1
    input_ls = json_file['coordinates']
    tmp_ls = json_file['templat_size']

    f1 = f1_score(groundtruth_ls=gorundtruth_ls, input_ls=input_ls, tp_h=tmp_ls[0], tp_w=tmp_ls[1])
    return f1


def get_name_ID(line):
    name = re.findall('_([a-z0-9]+)_attempt*', line)
    id = re.findall('\S*CSE4573PROJ1-([0-9]+).\S+', line)
    retname = name[0]
    retID = 00000000 if len(id) < 1 else id[0]
    return retname, retID


def create_dict(fieldnames, ubit, a1, a2, b1, b2, c11, c12, c21, c22):
    return {fieldnames[0]: ubit,
            fieldnames[1]: a1,
            fieldnames[2]: a2,
            fieldnames[3]: b1,
            fieldnames[4]: b2,
            fieldnames[5]: c11,
            fieldnames[6]: c12,
            fieldnames[7]: c21,
            fieldnames[8]: c22 }


def question2_grader_driver(script_folder_dir):
    # script_folder_dir = './proj2_Run/adearauj/adearauj/'
    a1 = (question2_grader(groundtruth_path="./a.csv",
                           json_path=os.path.join(script_folder_dir, 'auto_script_save', 'a.json')))
    a2 = (question2_grader(groundtruth_path="./a.csv",
                           json_path=os.path.join(script_folder_dir, 'results', 'a.json')))

    b1 = (question2_grader(groundtruth_path="./b.csv",
                           json_path=os.path.join(script_folder_dir, 'auto_script_save', 'b.json')))
    b2 = (question2_grader(groundtruth_path="./b.csv",
                           json_path=os.path.join(script_folder_dir, 'results', 'b.json')))

    c11 = (question2_grader(groundtruth_path="./c1.csv",
                            json_path=os.path.join(script_folder_dir, 'auto_script_save', 'c.json')))
    c12 = (question2_grader(groundtruth_path="./c1.csv",
                            json_path=os.path.join(script_folder_dir, 'results', 'c.json')))

    c21 = (question2_grader(groundtruth_path="./c2.csv",
                            json_path=os.path.join(script_folder_dir, 'auto_script_save', 'c.json')))
    c22 = (question2_grader(groundtruth_path="./c2.csv",
                            json_path=os.path.join(script_folder_dir, 'results', 'c.json')))
    return a1, a2, b1, b2, c11, c12, c21, c22


def main():
    work_dir = './proj2_addtl'
    csv_file = 'question2_score_new_2Run_1.csv'
    fieldnames = ['UBIT', 'F1_a1_Auto', 'F1_a2_st', 'F1_b1_Auto', 'F1_b2_st', 'F1_c11_Auto', 'F1_c12_st', 'F1_c21_Auto', 'F1_c22_st']

    onlyfiles = [f for f in os.listdir(work_dir) if os.path.isdir(os.path.join(work_dir, f))]

    for i in range(len(onlyfiles)):

        print('Progress: ', i+1, "/", len(onlyfiles))
        filename = onlyfiles[i]
        print(filename)

        # retrieve name
        name = filename

        # CHECK MODE
        # if name != 'moddiraj': continue

        # check if already graded!!!
        # TODO
        if search_csv(csv_file, name): continue

        # determine the directory to the script
        script_directory = os.path.join(work_dir, name)
        while len(os.listdir(script_directory)) == 1:
            # one more directory to go
            script_directory = os.path.join(script_directory, os.listdir(script_directory)[0])
        print("working dir: ", script_directory)


        # grading
        a1, a2, b1, b2, c11, c12, c21, c22 = question2_grader_driver(script_directory)

        # write to csv
        content = create_dict(fieldnames, name,
                              a1, a2, b1, b2, c11, c12, c21, c22)
        print(content)
        if os.path.isfile(csv_file):
            append_dict_as_row(csv_file, content, fieldnames)
        else:
            write_dict_as_row(csv_file, content, fieldnames)

        # clean the tmp work space
        # if os.path.isdir(work_dir): shutil.rmtree(work_dir)


if __name__ == "__main__":
    main()
