# !/usr/bin/env python
# encoding: utf-8
import argparse
import cv2
import shutil
import math
import os
import numpy as np

__version__ = "2022.10.08.01"
parser = argparse.ArgumentParser()

def version():
    return "version:" + __version__

def main():
    parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
    parser.add_argument('-t', '--type', type=str, default="single", help='compress type single file or folder or folder recursive.')
    parser.add_argument('-r', '--ratio', type=str, default="/home/image_root/ossRoot", help='Image root path')

    parser.add_argument('-o', '--outFolder', type=str, default="/home/jove-temp/images", help='Image export out folder')
    parser.add_argument('-f', '--filePaths', type=str, default="/home/jove-temp/uri.txt", help='Need Image uri paths')
    args = parser.parse_args()

def jpg(ratio, img):
    params = [cv2.IMWRITE_JPEG_QUALITY, ratio]  # ratio:0~100
    msg = cv2.imencode(".jpg", img, params)[1]
    msg = (np.array(msg)).tobytes()
    print("msg:", len(msg))

def png(ratio, img):
    params = [cv2.IMWRITE_PNG_COMPRESSION, ratio]  # ratio: 0~9
    msg = cv2.imencode(".png", img, params)[1]
    msg = (np.array(msg)).tobytes()

def compress_image(src: str, out: str) -> None:
    print(os.path.getsize(src))
    img = cv2.imread(src)
    jpg(90, img)
    cv2.imwrite(r"ret_9.png", img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    pass

if __name__ == '__main__':
    compress_image("/Users/user/Downloads/21efb65f-f24b-4cb1-9856-eff65a4717fc.jpg", "22")
    main()
