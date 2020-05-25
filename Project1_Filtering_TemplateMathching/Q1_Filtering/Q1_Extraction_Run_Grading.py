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

def normalization(input):
    """
    :param input: image
    :return: normalized image
    """
    input = np.asarray(input, dtype=np.float)
    std = np.std(input)
    std = 1 if std == 0 else std
    input = (input - np.mean(input)) / (std * len(input))
    return input


def normalizedCC(img1_dir, img2_dir):
    """
    :param img1_dir: image 1
    :param img2_dir: image 2
    :return:  NCC between the two
    """
    if not os.path.isfile(img1_dir): return 0
    if not os.path.isfile(img2_dir): return 0

    img1 = cv2.imread(img1_dir, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_dir, cv2.IMREAD_GRAYSCALE)
    img1 = normalization(img1)
    img2 = normalization(img2)
    score = signal.correlate2d(img1, img2, mode='valid')
    return score


def grading_q1(script_path, img_path, gt_dir, filter_type, time_out):
    """
    :param script_path: path to load the script
    :param img_path: path to read the image to be processed
    :param gt_dir: directory to load ground truth files
    :param filter_type:  filter name
    :param time_out: max wait time to run the script
    :return: status + 3 scores
    """
    # create tmp results folder if not exist
    save_path = os.path.join(script_path, "auto_script_save")
    if not os.path.isdir(os.path.join(save_path)):
        os.mkdir(os.path.join(save_path))

    print(os.path.isfile(os.path.join(script_path, "task1.py")))
    print(os.path.join(script_path, "task1.py"))
    # set arg parameters
    feed_arg = "python " + os.path.join(script_path, "task1.py") + \
               " --img_path " + img_path + \
               " --kernel " + filter_type + \
               " --result_saving_directory " + save_path
    print(feed_arg)
    # run the script
    status = False
    returncode = -999
    try:
        p = subprocess.run(shlex.split(feed_arg), timeout=time_out, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        status = True
    except:
        status = False
    if status:
        if not p.returncode == 0: status = False
        returncode = p.returncode
    print("return code: ", returncode)
    print("status: ", "success!" if status else "failed!")

    # cross-correlation
    if status:
        score1 = normalizedCC(os.path.join(gt_dir, filter_type + "_edge_x.jpg"),
                              os.path.join(save_path, filter_type + "_edge_x.jpg"))
        score2 = normalizedCC(os.path.join(gt_dir, filter_type + "_edge_y.jpg"),
                              os.path.join(save_path, filter_type + "_edge_y.jpg"))
        score3 = normalizedCC(os.path.join(gt_dir, filter_type + "_edge_mag.jpg"),
                              os.path.join(save_path, filter_type + "_edge_mag.jpg"))
        score = (returncode, status, abs(score1[0][0]), abs(score2[0][0]), abs(score3[0][0]))
    else:
        score = (returncode, status, 0, 0, 0)
    return score


def get_name_ID(line):
    """
    :param line: file name of the submission package
    :return: extract ubid from name via regular expression
    """
    name = re.findall('_([a-z0-9]+)_attempt*', line)
    id = re.findall('\S*CSE4573PROJ1-([0-9]+).\S+', line)
    retname = name[0]
    retID = 00000000 if len(id) < 1 else id[0]
    return retname, retID


def grading_q1_driver(script_path):
    # for grading question 1
    img_path = "./data/proj1-task1.jpg"
    gt_dit = "./groundtruth/"
    score1 = grading_q1(script_path, img_path, gt_dit, "prewitt", 200)
    score2 = grading_q1(script_path, img_path, gt_dit, "sobel", 200)
    print(score1)
    print(score2)
    return score1, score2


def create_dict(fieldnames, ubit, ubno, code1, status1, s1_1, s1_2, s1_3, code2, status2, s2_1, s2_2, s2_3):
    '''
    :return: create dictionary for ease of output to table
    '''
    return {fieldnames[0]:ubit,
            fieldnames[1]:ubno,
            fieldnames[2]:code1,
            fieldnames[3]:status1,
            fieldnames[4]:s1_1,
            fieldnames[5]:s1_2,
            fieldnames[6]:s1_3,
            fieldnames[7]:code2,
            fieldnames[8]:status2,
            fieldnames[9]:s2_1,
            fieldnames[10]:s2_2,
            fieldnames[11]:s2_3,}


def main():
    # dir to all zipped submissions
    submission_dir = "./All"

    # a tmp working folder, zipped package will be exported here
    work_dir = './tmp'

    # place to save running log
    csv_file = 'question1.csv'

    fieldnames = ['UBIT', 'UB#', 'Q1-T1-RetCode', 'Q1-T1-Status', 'Q1-T1-S1', 'Q1-T1-S2', 'Q1-T1-S3',
                  'Q1-T2-RetCode', 'Q1-T2-Status', 'Q1-T2-S1', 'Q1-T2-S2', 'Q1-T2-S3']

    onlyfiles = [f for f in os.listdir(submission_dir) if os.path.isfile(os.path.join(submission_dir, f))]

    for i in range(len(onlyfiles)):

        print('Progress: ', i, "/", len(onlyfiles))
        filename = onlyfiles[i]
        print(filename)

        # retrieve name
        name, ID = get_name_ID(filename)

        # CHECK MODE
        if name != 'moddiraj': continue

        # check if already graded!!!
        # TODO
        # if search_csv(csv_file, name): continue

        # create tmp folder
        if not os.path.isdir(work_dir):
            os.mkdir(work_dir)

        # extract zip file
        print(os.path.join(submission_dir, filename))
        with zipfile.ZipFile(os.path.join(submission_dir, filename), 'r') as zip_ref:
            zip_ref.extractall(work_dir)

        # determine the directory to the script
        script_directory = work_dir
        while len(os.listdir(script_directory)) == 1:
            # one more directory to go
            os.rename(os.path.join(script_directory,os.listdir(script_directory)[0]),
                      os.path.join(script_directory, "proj1"))
            script_directory = os.path.join(script_directory, os.listdir(script_directory)[0])
        # print(script_directory)

        # grading
        score1, score2 = grading_q1_driver(script_directory)

        # write to csv
        content = create_dict(fieldnames, name, ID,
                              score1[0], score1[1], score1[2], score1[3], score1[4],
                              score2[0], score2[1], score2[2], score2[3], score2[4])
        print(content)
        if os.path.isfile(csv_file):
            append_dict_as_row(csv_file, content, fieldnames)
        else:
            write_dict_as_row(csv_file, content, fieldnames)

        # clean the tmp work space
        # if os.path.isdir(work_dir): shutil.rmtree(work_dir)






if __name__ == "__main__":
    main()
