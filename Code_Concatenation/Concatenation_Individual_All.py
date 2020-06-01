import shutil
import zipfile

from Utils import *

import os



def main():
    '''
    combine all py files in the submission folder
    exclude the handout py files

    return: each student will result in only one py file which was composed of all py files they submitted.
    '''

    # root directory to previous year's submission
    zip_dir = "../Downloaded/res00043"

    # a tmp location to unzip each zipped package
    work_dir = "./tmp"

    # output folder
    out_dir =  "./out"

    # some students like to include exmaple files we handout to them, need to exclude those files in concenation to avoid potential falsealarm
    bkls = ["ComputeFBeta", "create_json_sample"]

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)

    for fd in os.listdir(zip_dir):
        print("processing: ", fd)

        if os.path.isfile(os.path.join(out_dir, fd+".py")):
            print("already done, skip!")
            continue

        zip_file = os.listdir(os.path.join(zip_dir, fd))[0]
        print("file inside: ", zip_file)

        # check if is zip
        check = re.search("\S+zip$", zip_file)
        if check == None :
            print("not a zip, pass")
            continue


        tmp_work_dir = os.path.join(work_dir, fd)
        if not os.path.isdir(tmp_work_dir):
            os.mkdir(tmp_work_dir)
       

        # determine the directory to the script
        script_directory = tmp_work_dir

        # check if macosx
        for dir in os.listdir(script_directory):
            if "MACOSX" in dir:
                shutil.rmtree(os.path.join(script_directory, dir))

        while len(os.listdir(script_directory)) == 1:
            # one more directory to go
            os.rename(os.path.join(script_directory, os.listdir(script_directory)[0]),
                      os.path.join(script_directory, fd))
            script_directory = os.path.join(script_directory, os.listdir(script_directory)[0])
        print("script located in: ", script_directory)

        all_pys = get_all_py_in_dir_all(script_directory, bkls)
        print("founded pys: ")
        for xxxx in all_pys:
            print(xxxx)
        out_file_name = os.path.join(out_dir, fd+".py")
        combine(all_pys, out_file_name, zip_file, fd,  os.listdir(script_directory))
        print("saved to: ", out_file_name)


if __name__ == "__main__":
    main()

