# !/usr/bin/env python
# encoding: utf-8
import argparse
import pathlib

import cv2
import shutil
import math
import os
import numpy as np

__version__ = "2022.10.08.01"
parser = argparse.ArgumentParser()


def version():
    return "version:" + __version__


parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
parser.add_argument('-t', '--type', type=str, default="folder", choices=['single', 'folder', 'folder-r'],
                    help='compress type single file or folder or folder recursive.')
parser.add_argument('-r', '--ratio', type=int, default=90, help='Image ratio')
parser.add_argument('-i', '--inputFolder', type=str, help='Image input folder')
parser.add_argument('-o', '--outFolder', type=str, help='Image export out folder')
parser.add_argument('-g', '--gary', type=bool, default=False, help='transfer to gary')
args = parser.parse_args()

type = args.type
rate = args.ratio
inputFolder = args.inputFolder
outputFolder = args.outFolder
gary = args.gary


def jpg(ratio, img):
    params = [cv2.IMWRITE_JPEG_QUALITY, ratio * 10]  # ratio:0~100
    msg = cv2.imencode(".jpg", img, params)[1]
    msg = (np.array(msg)).tobytes()
    img = cv2.imdecode(np.frombuffer(msg, np.uint8), cv2.IMREAD_COLOR)
    return img


def png(ratio, img):
    params = [cv2.IMWRITE_PNG_COMPRESSION, ratio]  # ratio: 0~9
    msg = cv2.imencode(".png", img, params)[1]
    msg = (np.array(msg)).tobytes()
    img = cv2.imdecode(np.frombuffer(msg, np.uint8), cv2.IMREAD_COLOR)
    return img


def just_copy(src, out):
    if os.path.isfile(src) is False or os.path.isdir(out) is False:
        print("参数错误")
        return
    p = pathlib.Path(src)
    shutil.copyfile(src, os.path.join(out, p.name))


def single_compress_image(src, out, rate=9, gary=False):
    if os.path.isfile(src) is False or os.path.isdir(out) is False:
        print("src :" + src + "is not image")
        return
    p = pathlib.Path(src)  # test.py
    base_name = p.stem
    suffix = check_image(src)
    if suffix is None:
        print("src :" + src + "is not image")
        return
    size = os.path.getsize(src)
    if gary is False and size < 1024 * 20:
        just_copy(src, out)
        print("copy succ: " + src)
        return
    if suffix.upper() != ".PNG":
        suffix = '.jpg'
    img = cv2.imread(src)
    if gary:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if os.path.exists(out) is False:
        os.makedirs(out, exist_ok=False)
    if suffix.upper() == '.JPG':
        rate = rate * 10
    if size < 1024 * 20:
        cv2.imwrite(os.path.join(out, os.path.join(out, p.name)), img)
    if suffix.upper() == ".PNG":
        cv2.imwrite(os.path.join(out, base_name + suffix), img, [cv2.IMWRITE_PNG_COMPRESSION, rate])
    else:
        cv2.imwrite(os.path.join(out, base_name + suffix), img, [cv2.IMWRITE_JPEG_QUALITY, rate])
    print("copy succ: " + src)

def folder_compress_image(src, out, rate=9, gary=False):
    if os.path.isdir(src) is False or os.path.isdir(out) is False:
        print("参数错误")
        return
    for file in os.listdir(src):
        single_compress_image(os.path.join(src, file), out, rate, gary)

def check_image(path: str) -> str:
    p = pathlib.Path(path)
    suffix = p.suffix
    if suffix is None or suffix == '':
        return None
    if suffix.upper() in ('.JPG', '.PNG', '.BMP', '.JPEJ'):
        return suffix.lower()
    return None



if __name__ == '__main__':
    print(args)
    if type == 'single':
        single_compress_image(inputFolder, outputFolder, rate, gary)
    elif type == 'folder':
        if os.path.exists(outputFolder) is False:
            os.makedirs(outputFolder, exist_ok=False)
        folder_compress_image(inputFolder, outputFolder, rate, gary)
    else:
        print("wait update ")
