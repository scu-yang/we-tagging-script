# !/usr/bin/env python
# encoding: utf-8
import argparse
import shutil
import os

__version__ = "2022.10.08"

def version():
    return "version:" + __version__

def read_image(uri, root, out):
    for line in open(uri, 'r'):
        line = line.strip()
        if len(line) == 0:
            continue
        inFile = root + line
        arr = line.split("//")
        out = out + "/" + arr[-1:][0]
        shutil.copyfile(inFile, out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
    parser.add_argument('-r', '--imageRoot', type=str, default="/home/image_root/ossRoot", help='Image root path')
    parser.add_argument('-o', '--outFolder', type=str, default="/home/jove-temp/images", help='Image export out folder')
    parser.add_argument('-f', '--filePaths', type=str, default="/home/jove-temp/uri.txt", help='Need Image uri paths')
    args = parser.parse_args()
    if os.path.exists(args.outFolder) is False:
        os.makedirs(args.outFolder, exist_ok=False)
    read_image(args.filePaths, args.imageRoot, args.outFolder)