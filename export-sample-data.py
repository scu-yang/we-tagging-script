# !/usr/bin/env python
# encoding: utf-8
import argparse
import pathlib

import cv2
import shutil
import math
import os
import numpy as np

def version():
    return "version:" + __version__

__version__ = "2022.10.08.01"
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
parser.add_argument('-i', '--inputFolder', type=str, help='Image input folder')
parser.add_argument('-o', '--outputFolder', type=str, help='Image export out folder')

def version():
    return "version:" + __version__


def main(inputFolder, outputFolder):
    folder = inputFolder
    outFolder = outputFolder

    for sub in os.listdir(folder):
        subPath = os.path.join(folder, sub)
        outSubPath = os.path.join(outFolder, sub)
        if os.path.exists(outSubPath) is False:
            os.makedirs(outSubPath, exist_ok=False)
        index = 0
        for file in os.listdir(subPath):
            outFile = os.path.join(outSubPath, file)
            shutil.copyfile(os.path.join(subPath, file), os.path.join(outSubPath, file))
            index += 1
            if index > 20:
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    inputFolder = parser.inputFolder
    outputFolder = parser.outputFolder
    main(inputFolder, outputFolder)