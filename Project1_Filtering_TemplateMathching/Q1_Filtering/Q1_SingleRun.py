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


def grading_q1(script_path, img_path, filter_type, time_out):
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
    print("status code: ", status)
    print("status: ", "success!" if status else "failed!")

    return


def get_name_ID(line):
    name = re.findall('_([a-z0-9]+)_attempt*', line)
    id = re.findall('\S*CSE4573PROJ1-([0-9]+).\S+', line)
    retname = name[0]
    retID = 00000000 if len(id) < 1 else id[0]
    return retname, retID


def grading_q1_driver(script_path):
    # for grading question 1
    img_path = "./data/proj1-task1.jpg"

    grading_q1(script_path, img_path, "prewitt", 200)

    grading_q1(script_path, img_path, "sobel", 200)

    return


def main():
    # determine the directory to the script
    script_directory = "./proj3_addtl/javiaire/javiaire/"

    # grading
    grading_q1_driver(script_directory)


if __name__ == "__main__":
    main()
