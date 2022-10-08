# !/usr/bin/env python
# encoding: utf-8
import argparse
import shutil
import os
import pathlib

__version__ = "2022.10.08"

def version():
    return "version:" + __version__

train = 0.8
test = 0.1
val = 0.1
images_folder = "blood-cells-label-export/out-images"
label_folder = "blood-cells-label-export/out-labels"
out_folder = "blood-cells-label-export"

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
parser.add_argument('-t', '--train', type=float, default=0.7, help='train set size ratio')
parser.add_argument('-e', '--test', type=float, default=0.2, help='test set size ratio')
parser.add_argument('-a', '--val', type=float, default=0.1, help='val set size ratio')
parser.add_argument('-i', '--imagesFolder', type=str, default="blood-cells-label-export/out-images", help='images folder')
parser.add_argument('-l', '--labelFolder', type=str, default="blood-cells-label-export/out-labels", help='labels folder')
parser.add_argument('-o', '--outFolder', type=str, default="blood-cells-label-export/data-set", help='out folder')
args = parser.parse_args()
train = args.train
test = args.test
val = args.val
images_folder = args.imagesFolder
label_folder = args.labelFolder
out_folder = args.outFolder

if os.path.exists(images_folder) is False:
    os.makedirs(images_folder, exist_ok=False)
if os.path.exists(label_folder) is False:
    os.makedirs(label_folder, exist_ok=False)
if os.path.exists(out_folder) is False:
    os.makedirs(out_folder, exist_ok=False)


train_r = 1.0 * train / (train + test + val)
test_r = 1.0 * test / (train + test + val)
val_r = 1.0 * val / (train + test + val)

def move_image_label(type, images):
    out_labels_folder = out_folder + "/" + type + "/labels"
    out_images_folder = out_folder + "/" + type + "/images"
    if os.path.exists(out_labels_folder) is False:
        os.makedirs(out_labels_folder, exist_ok=False)
    if os.path.exists(out_images_folder) is False:
        os.makedirs(out_images_folder, exist_ok=False)
    for image in images:
        p = pathlib.Path(image)  # test.py
        base_name = p.stem
        target_label = label_folder + "/" + base_name + '.txt'
        target_image = images_folder + "/" + image
        new_label = out_labels_folder + "/" + base_name + '.txt'
        new_image = out_images_folder + "/" + image
        shutil.copyfile(target_label, new_label)
        shutil.copyfile(target_image, new_image)

def read_images(images_folder):
    images = os.listdir(images_folder)
    n = len(images)
    train_index = int(train_r*n)
    test_index = int((train_r+test_r)*n)
    train_images = images[0: train_index]
    test_images = images[train_index:test_index]
    var_images = images[test_index:]
    move_image_label("train", train_images)
    move_image_label("test", test_images)
    move_image_label("var", var_images)

if __name__ == '__main__':
    read_images(images_folder)
