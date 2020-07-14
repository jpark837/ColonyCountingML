import os
import cv2
import shutil

def get_path(i):

    script_dir = os.path.dirname(__file__)
    abs_dir_path = os.path.join(script_dir, "binary_masked")

    rel_path = "".join(["colony image masked(",str(i),").jpg"])
    abs_file_path = os.path.join(abs_dir_path, rel_path)
    os.path.normpath(abs_file_path)

    return abs_file_path

def resize(abs_file_path):

    oriimg = cv2.imread(abs_file_path, 0) # read image
    img = cv2.resize(oriimg,(400,400))

    return img

def save(i,img):
    script_dir = os.path.dirname(__file__)
    abs_dir_path = os.path.join(script_dir, "binary_masked_resized")

    rel_path = "".join(["colony image resized(",str(i),").jpg"])
    abs_file_path = os.path.join(abs_dir_path, rel_path)
    os.path.normpath(abs_file_path)
    cv2.imwrite(abs_file_path, img)

    return

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    abs_dir_path = os.path.join(script_dir, "binary_masked_resized")

    # check if directory exists
    flag = os.path.isdir(abs_dir_path)
    if flag is True:
        shutil.rmtree(abs_dir_path)

    os.mkdir(abs_dir_path)

    for i in range(0,32):
        abs_file_path = get_path(i+1)
        img = resize(abs_file_path)
        save(i+1,img)