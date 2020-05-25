import os
import re
import csv
import json




def get_all_py_in_dir_all(dir, blackls):

    out = []

    for f in os.listdir(dir):
        xx = re.search("^_\S+", f)
        if xx is not None:
            continue

        curr = os.path.join(dir, f)

        if os.path.isfile(curr):
            # if it is a file
            xx = re.search("\S+\.py$", f)
            if xx is not None:
                flag = False
                for bk in blackls:
                    if bk.lower() in f.lower():
                        flag = True
                        break
                if flag: continue
                out.append(curr)

        else:
            # if it is a folder
            pys = get_all_py_in_dir_all(curr, blackls)
            if len(pys) > 0 :
                out.extend(pys)

    return out


def combine( file_ls, out_file_name, zipname, archive_dir, dir_ls):

    all_contents = []

    all_contents.append("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    all_contents.append("Archive Dir: " + archive_dir)
    all_contents.append("Archive Name: " + zipname )
    all_contents.append("PY Files in zip:")

    for i, tmp in enumerate(file_ls):
        all_contents.append("\t" + str(i+1) + " " + tmp)

    all_contents.append(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    for file in file_ls:
        all_contents.append("\n###################################################")
        all_contents.append("# Inner File: " + file)
        all_contents.append("###################################################\n")

        with open(os.path.join( file)) as f:
            lines = f.read().splitlines()
        all_contents.extend(lines)

    all_contents.append("\n\n\n")

    with open(out_file_name, 'w') as f:
        for line in all_contents:
            f.write(line + '\n')

    return










'''
old
'''



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




