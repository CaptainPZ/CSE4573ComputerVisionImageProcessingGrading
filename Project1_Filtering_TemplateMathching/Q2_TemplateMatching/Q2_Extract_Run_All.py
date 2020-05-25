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
from csvwriter import modify
from csvwriter import checkIfImplemented



def runner(script_path, time_out, char_name, root_dir):
    """
    :param script_path: path to load the script
    :param time_out: max wait time to run the script
    :return: status + 3 scores
    """
    # create tmp results folder if not exist

    os.chdir(script_path)
    script_path = "./"

    save_path = os.path.join(script_path, "auto_script_save")
    if not os.path.isdir(os.path.join(save_path)):
        os.mkdir(os.path.join(save_path))

    script_dir = os.path.join(script_path, "task2.py")
    img_path = os.path.join(script_path, 'data', 'proj1-task2-png.png')
    tmplate_path = get_template_dir(script_path, char_name)

    # Initialize Status
    status = False
    returncode = -999

    # check if implemented
    if not checkIfImplemented(script_dir):
        os.chdir(root_dir)
        return returncode, status
    if tmplate_path is None:
        os.chdir(root_dir)
        return returncode, status

    # set arg parameters
    feed_arg = "python " + script_dir + \
               " --img_path " + img_path + \
               " --template_path " + tmplate_path + \
               " --result_saving_directory " + save_path
    print(feed_arg)

    # run script
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

    os.chdir(root_dir)
    return returncode, status


def runner_driver(script_path, root_dir):
    a1, a2 = runner(script_path, 3000, "a", root_dir)
    b1, b2 = runner(script_path, 3000, "b", root_dir)
    c1, c2 = runner(script_path, 3000, "c", root_dir)
    return (a1, a2, b1,b2, c1, c2)



def get_name_ID(line):
    name = re.findall('_([a-z0-9]+)_attempt*', line)
    id = re.findall('\S*CSE4573PROJ1-([0-9]+).\S+', line)
    retname = name[0]
    retID = 00000000 if len(id) < 1 else id[0]
    return retname, retID


def get_template_dir(script_path, template_name):
    dir = os.path.join(script_path, 'data')
    onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    for file in onlyfiles:
        if(file.startswith(template_name+'.')):
            return os.path.join(dir, file)
    return None


def create_dict(fieldnames, ubit, ubno, a1, a2, b1, b2, c1, c2):
    return {fieldnames[0]:ubit,
            fieldnames[1]:ubno,
            fieldnames[2]:a1,
            fieldnames[3]:a2,
            fieldnames[4]:b1,
            fieldnames[5]:b2,
            fieldnames[6]:c1,
            fieldnames[7]:c2}



def main():

    root_dir = "/home/bigbro/Downloads/2020SpringGrading"
    os.chdir(root_dir)

    submission_dir = "./All/new"
    work_dir = './proj2_addtl'
    fieldnames = ['UBIT', 'UB#', 'a-RetCode', 'a-Status','b-RetCode', 'b-Status','c-RetCode', 'c-Status']
    csv_file = 'question2_2_runlog.csv'

    onlyfiles = [f for f in os.listdir(submission_dir) if os.path.isfile(os.path.join(submission_dir, f))]
    # print(onlyfiles[47])
    # exit()

    for i in range(len(onlyfiles)):
        os.chdir(root_dir)

        print('Progress: ', i, "/", len(onlyfiles))
        filename = onlyfiles[i]
        print("Processing: ", filename)

        # retrieve name
        name, ID = get_name_ID(filename)

        # CHECK MODE
        # if name != 'moddiraj': continue


        # create tmp folder
        if not os.path.isdir(work_dir):
            os.mkdir(work_dir)


        # check if already extracted!!!
        # TODO
        if search_csv(csv_file, name):
            print("found finished, skip!")
            continue
        if os.path.isdir(os.path.join(work_dir, name)):
            print("found folder: ", os.path.join(work_dir, name), " deleting...")
            shutil.rmtree(os.path.join(work_dir, name))
            print("deleted!")

        # create wor_dir_name
        if not os.path.isdir(os.path.join(work_dir, name)):
            os.mkdir(os.path.join(work_dir, name))

        tmp_work_dir = os.path.join(work_dir, name)

        # extract zip file
        print("extracting: ", os.path.join(submission_dir, filename),
              "\n\tto:", tmp_work_dir)
        with zipfile.ZipFile(os.path.join(submission_dir, filename), 'r') as zip_ref:
            zip_ref.extractall(tmp_work_dir)

        # determine the directory to the script
        script_directory = tmp_work_dir

        # check if macosx
        for dir in os.listdir(script_directory):
            if "MACOSX" in dir:
                shutil.rmtree(os.path.join(script_directory, dir))

        while len(os.listdir(script_directory)) == 1:
            # one more directory to go
            os.rename(os.path.join(script_directory,os.listdir(script_directory)[0]),
                      os.path.join(script_directory, name))
            script_directory = os.path.join(script_directory, os.listdir(script_directory)[0])
        print("script located in: ", script_directory)
        modify(os.path.join(script_directory, "task2.py"))

        # check img file existence
        if not os.path.isfile(os.path.join(script_directory, 'data', 'proj1-task2-png.png')):
            source = os.path.join(root_dir,'data', 'proj1-task2-png.png')
            dest = os.path.join(script_directory,'data', 'proj1-task2-png.png')
            shutil.copyfile(source, dest)

        # running
        a1,a2, b1, b2, c1, c2 = runner_driver(script_directory, root_dir)

        # write to csv
        content = create_dict(fieldnames, name, ID,a1,a2, b1, b2, c1, c2)
        print(content)
        if os.path.isfile(csv_file):
            append_dict_as_row(csv_file, content, fieldnames)
        else:
            write_dict_as_row(csv_file, content, fieldnames)

        # clean the tmp work space
        # if os.path.isdir(work_dir): shutil.rmtree(work_dir)



if __name__ == "__main__":
    main()
