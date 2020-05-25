import copy
import json
import os
import cv2


def show_image(img):
    """Shows an image.
    """
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('image', img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def read_json(file_name):
    try:
        with open(file_name) as f:
            data = json.load(f)
    except:
        data = None
    if data == None:
        return None, None
    input_ls = data['coordinates']
    tmp_ls = data['templat_size']
    return input_ls, tmp_ls


def show_img(img_path, json_path1, json_path2):
    img = cv2.imread(img_path)
    input_ls, tmp_ls = read_json(json_path1)

    if input_ls != None:
        for coord in input_ls:
            r = int(coord[0]) + 0.5 * int(tmp_ls[0])
            c = int(coord[1]) + 0.5 * int(tmp_ls[1])
            cv2.circle(img, (int(c), int(r)), 7, (0, 0, 255))

    input_ls, tmp_ls = read_json(json_path2)
    if input_ls != None:
        for coord in input_ls:
            r = int(coord[0]) + 0.5 * int(tmp_ls[0])
            c = int(coord[1]) + 0.5 * int(tmp_ls[1])
            cv2.circle(img, (int(c), int(r)), 5, (255, 0, 0))
    show_image(img)



def show_img2(img_path, json_path1, json_path2):
    img = cv2.imread(img_path)
    input_ls, tmp_ls = read_json(json_path1)
    if input_ls != None:
        for coord in input_ls:
            r = int(coord[0]) + 0.5 * int(tmp_ls[0])
            c = int(coord[1]) + 0.5 * int(tmp_ls[1])
            cv2.circle(img, (int(r), int(c)), 7, (0, 0, 255))

    input_ls, tmp_ls = read_json(json_path2)
    if input_ls != None:
        for coord in input_ls:
            r = int(coord[0]) + 0.5 * int(tmp_ls[0])
            c = int(coord[1]) + 0.5 * int(tmp_ls[1])
            cv2.circle(img, (int(r), int(c)), 5, (255, 0, 0))
    show_image(img)


work_dir = './proj2_Run_3'
name = "twperiso"
char = "a"

# determine the directory to the script
script_directory = os.path.join(work_dir, name)
while len(os.listdir(script_directory)) == 1:
    # one more directory to go
    script_directory = os.path.join(script_directory, os.listdir(script_directory)[0])
print("working dir: ", script_directory)

scp_dir = script_directory
# auto in red
show_img('./data/proj1-task2-png.png', os.path.join(scp_dir,"auto_script_save",char+".json"),
         os.path.join(scp_dir,"results",char+".json"))

show_img2('./data/proj1-task2-png.png', os.path.join(scp_dir,"auto_script_save",char+".json"),
         os.path.join(scp_dir,"results",char+".json"))