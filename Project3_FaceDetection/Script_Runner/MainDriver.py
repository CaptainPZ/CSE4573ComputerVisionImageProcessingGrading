import shutil
import zipfile
import shlex
import subprocess

from Grading_Script.Utils import *
from True_Grading.utility import *

import os



def runner(script_path):


    os.chdir(script_path)
    script_path = "./"

    script_dir = get_face_py(script_path)


    # Initialize Status
    status = False
    returncode = -999

    if script_dir is None:
        return returncode, status

    # set arg parameters
    feed_arg = "python " + script_dir + \
               " " + "./auto_test"
    print(feed_arg)

    # run script
    try:
        p = subprocess.run(shlex.split(feed_arg), timeout=600, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        status = True
    except:
        status = False
    if status:
        if not p.returncode == 0: status = False
        returncode = p.returncode
    print("return code: ", returncode)
    print("status: ", "success!" if status else "failed!")
    return returncode, status


def main():
    # dir where this script resides, easy for code to navigate back
    root_dir = "/home/bigbro/Downloads/2020SpringGrading3/True_Grading/"
    os.chdir(root_dir)

    # dir to submissions
    zip_dir = "../Downloaded/face"

    # tmp work dir
    work_dir = "./tmp"

    # result csv folder
    out_dir =  "./out"

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)

    for fd in os.listdir(zip_dir):
        os.chdir(root_dir)
        print("processing: ", fd)
        person_name = get_name(fd)
        print("name: ", person_name)

        # if os.path.isdir(os.path.join(out_dir, person_name)):
        #     print("already done, skip!")
        #     continue

        zip_file =os.path.join(zip_dir, fd)
        print("file: ", zip_file)

        # check if is zip
        check = re.search("\S+zip$", zip_file)
        if check == None :
            print("not a zip, pass")
            continue

        # check if done!
        xx = search_csv("./out/out_summary.csv", person_name)
        if xx:
            print("done already in csv")
            continue

        tmp_work_dir = os.path.join(work_dir, person_name)
        if not os.path.isdir(tmp_work_dir):
            os.mkdir(tmp_work_dir)

        # extract zip file
        print("extracting: ", zip_file,
              "\n\tto:", tmp_work_dir)
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(tmp_work_dir)

        # determine the directory to the script
        script_directory = tmp_work_dir

        # check if macosx
        for dir in os.listdir(script_directory):
            if "MACOSX" in dir:
                shutil.rmtree(os.path.join(script_directory, dir))

        while len(os.listdir(script_directory)) == 1:
            # one more directory to go
            os.rename(os.path.join(script_directory, os.listdir(script_directory)[0]),
                      os.path.join(script_directory, person_name))
            script_directory = os.path.join(script_directory, os.listdir(script_directory)[0])
        print("script located in: ", script_directory)


        # copy test img
        test_dir = os.path.join(script_directory, "auto_test")
        if not os.path.isdir(test_dir):
            os.mkdir(test_dir)
        source = "./test_images/800.jpg"
        shutil.copyfile(source, os.path.join(test_dir, "800.jpg"))
        print("test image copied to folder: ", test_dir)

        # reserve submitted json
        submitted = json_to_string(os.path.join( script_directory,"results.json"), "800.jpg")
        print("found submitted: ", submitted)
        # remove old
        if os.path.isfile(os.path.join(script_directory, "results.json")):
            os.remove(os.path.join(script_directory, "results.json"))
            print("old json removed!")

        # run script
        returncode, status = runner(script_directory)

        # json file
        # generated
        generated = json_to_string("./auto_test/results.json", "800.jpg")
        if len(generated) == 0:
            generated = json_to_string("./results.json", "800.jpg")
            if len(generated) > 0:
                generated = "root " + generated

        # save results
        os.chdir(root_dir)
        out_dic = dict()
        header = ["name", "returncode", "status", "generated", "submitted"]
        out_dic["name"] = person_name
        out_dic["returncode"] = returncode
        out_dic["status"] = status
        out_dic["generated"] = generated
        out_dic["submitted"] = submitted

        write_to_csv("./out/out_summary.csv", out_dic, header)



if __name__ == "__main__":
    main()

