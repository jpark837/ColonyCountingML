import cv2
import numpy as np
import shutil
import os

def get_path(i):

    script_dir = os.path.dirname(__file__)
    abs_dir_path = os.path.join(script_dir, "binary")

    rel_path = "".join(["colony image binary(",str(i),").jpg"])
    abs_file_path = os.path.join(abs_dir_path, rel_path)
    os.path.normpath(abs_file_path)

    return abs_file_path

def remove_binary(abs_file_path):

    img = cv2.imread(abs_file_path, 0) # read image
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary

    height, width = img.shape[:2]
    total_pixels = height * width
    mask_white_pixel_thresh = total_pixels * 200 / 360000 # min number of white pixels changes with image size

    n_white_pix = np.sum(img == 255)
    n_black_pix = np.sum(img == 0)

    if n_white_pix > n_black_pix: # if original image is mainly white
        cv2.bitwise_not(img, img)

    finalimage = img.copy()

    num_labels, labels = cv2.connectedComponents(img) # find connected component
    mask = np.array(labels, dtype=np.uint8)
    for label in range(1,num_labels):
        new_mask = np.array(labels, dtype=np.uint8)

        new_mask[labels == label] = 255
        mask_white_pix = np.sum(new_mask == 255)
        if mask_white_pix > mask_white_pixel_thresh:
            mask[labels == label] = 255
        else:
            mask[labels == label] = 0

    cv2.bitwise_not(finalimage, finalimage, mask)

    if n_white_pix > n_black_pix:
        cv2.bitwise_not(finalimage, finalimage)

    return finalimage


def save_remove_binary(i,finalimage):
    script_dir = os.path.dirname(__file__)
    abs_dir_path = os.path.join(script_dir, "binary_masked")

    rel_path = "".join(["colony image masked(",str(i),").jpg"])
    abs_file_path = os.path.join(abs_dir_path, rel_path)
    os.path.normpath(abs_file_path)
    cv2.imwrite(abs_file_path, finalimage)
    return

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    abs_dir_path = os.path.join(script_dir, "binary_masked")

    # check if directory exists
    flag = os.path.isdir(abs_dir_path)
    if flag is True:
        shutil.rmtree(abs_dir_path)

    os.mkdir(abs_dir_path)

    for i in range(0,32):
        abs_file_path = get_path(i+1)
        finalimage = remove_binary(abs_file_path)
        save_remove_binary(i+1, finalimage)

    kmeans(abs_file_path)