# !/usr/bin/env python
# encoding: utf-8
import argparse
import shutil
import math

__version__ = "0.1.0"

uri = None
imageRoot = None
outFolder = None
parser = argparse.ArgumentParser()


def version():
    return "version:" + __version__


def read_image():
    for line in open(uri, 'r'):
        line = line.strip()
        if len(line) == 0:
            continue
        inFile = imageRoot + line
        arr = line.split("/")
        out = outFolder + "/" + arr[-1:][0]
        shutil.copyfile(inFile, out)


def main():
    parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
    parser.add_argument('-r', '--imageRoot', type=str, default="/home/image_root/ossRoot", help='Image root path')
    parser.add_argument('-o', '--outFolder', type=str, default="/home/jove-temp/images", help='Image export out folder')
    parser.add_argument('-f', '--filePaths', type=str, default="/home/jove-temp/uri.txt", help='Need Image uri paths')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
