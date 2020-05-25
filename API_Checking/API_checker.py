from helper import *
import os


def search_script(file_path, key_ls):
    ret = []
    if not os.path.isfile(file_path):
        return ret
    else:
        with open(file_path) as f:
            lines = f.read().splitlines()
        line_number = 0
        for line in lines:
            line = line.rstrip()
            line = line.lower()
            line_number += 1
            for key in key_ls:
                key = key.lower()
                if key in line:
                    ret.append((line_number, key, line))
        return ret


def make_dict(header, contents):
    out = dict();
    for header, content in zip(header, contents):
        out[header] = content
    return out


def main():
    # output file name
    csv_out = "API_check_3.csv"

    # directory to all py files
    folder = "./submissions20200503-110285-155koes"

    # key words to be checked
    key_set = ["BruteForce", "cv2.DescriptorMatcher_create", "DescriptorMatcher_create", "knnMatch", "findHomography",
               "BFMatcher", "Stitcher.create"]

    csv_header = ["file_name", "line_number", "matched_key_word", "original code"]

    for file in os.listdir(folder):
        print("checking: ", file)
        retls = search_script(os.path.join(folder, file), key_set)
        for line_no, key_word, line_code in retls:
            write_out_csv(csv_out, make_dict(csv_header, [file, line_no, key_word, line_code]), csv_header)

    print("done!")

if __name__ ==  "__main__":
    main()