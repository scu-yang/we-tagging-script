# !/usr/bin/env python
# encoding: utf-8
import argparse

import numpy as np
import pandas as pd
import os

__version__ = "2022.10.08"

def version():
    return "version:" + __version__

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
parser.add_argument('-c', '--labelConfig', type=str, help='label config file path')
parser.add_argument('-d', '--labelData', type=str,  help='label data file path')
parser.add_argument('-o', '--labelOutData', type=str,  help='label data file path')
parser.add_argument('-l', '--outLabelFolder', type=str,  help='out label folder')
parser.add_argument('-i', '--outUriFolder', type=str,  help='out uri folder')

args = parser.parse_args()
if os.path.exists(args.outUriFolder) is False:
    os.makedirs(args.outUriFolder, exist_ok=False)
if os.path.exists(args.outLabelFolder) is False:
    os.makedirs(args.outLabelFolder, exist_ok=False)




class_map = {
    5: 0,
    7: 1,
    9: 2,
    13: 3,
    11: 4
}


def transfer_label_class(data, needTransfer=True):
    """
    :param data: : pd.DataFrame
    :param needTransfer:
    :return:  -> pd.DataFrame
    """
    def get_class_code(x):
        categoryId = x['category_id']
        classId = x['class_id']
        if classId is None or classId == '' or pd.isna(classId):
            classId = 'None'
        map_key = "{}:{}".format(str(categoryId), str(classId))
        return class_map.get(map_key)
    if needTransfer:
        data["class_code"] = data.apply(get_class_code, axis=1)
    else:
        data["class_code"] = 0
    return data


def max_min_limit(data):
    """
    :param data: pd.DataFrame
    :return:  -> pd.DataFrame
    """
    def max_min(x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return x
    data['coordinate_x'] = data['coordinate_x'].apply(max_min)
    data['coordinate_y'] = data['coordinate_y'].apply(max_min)
    data['width'] = data['width'].apply(max_min)
    data['height'] = data['height'].apply(max_min)
    return data


def save_labels(label_path, data) :
    """
    :param label_path:
    :param data: pd.DataFrame
    :return: -> None
    """
    grouped = data.groupby('md5')
    for name, group in grouped:
        fileName = label_path + "/{}.txt".format(name)
        out = group[['class_code', 'coordinate_x', 'coordinate_y', 'width', 'height']]
        out.to_csv(fileName, encoding='utf-8', header=False, index=False, sep=" ")


def save_all_image_uri(folder, data):
    """
    :param folder:
    :param data: pd.DataFrame
    :return:  -> None
    """
    uri = data['uri'].unique()
    with open(folder + "/uri.txt", 'w') as f:
        for item in uri:
            f.write(item)
            f.write("\n")


def read_label_map(config_path):
    """
    :param config_path: str
    :return:  -> dict
    """
    config = pd.read_csv(config_path, encoding='utf-8')
    result = {}
    for row in config.iterrows():
        categoryId = row[1]['category_id']
        classId = row[1]['class_id']
        className = row[1]['class_name']
        classCode = row[1]['class_code']
        if className == '-':
            classId = 'None'
        map_key = "{}:{}".format(categoryId, classId)
        result[map_key] = str(classCode)
    return result


if __name__ == '__main__':
    labelConfigPath = args.labelConfig
    labelDataPath = args.labelData
    labelOutDataPath = args.labelOutData
    outLabelFolder = args.outLabelFolder
    outUriFolder = args.outUriFolder


    class_map = read_label_map(labelConfigPath)
    labels = pd.read_csv(labelDataPath
                         , encoding='utf-8'
                         , dtype={"class_id": str,
                                  'category_id': str,
                                  'img_id': str,
                                  "coordinate_x": np.float64,
                                  "coordinate_y": np.float64,
                                  "width": np.float64,
                                  "height": np.float64,
                                  "uri": str,
                                  "md5": str,
                                  "class_code": str})
    # 生成标签编码
    labels = transfer_label_class(labels)
    labels = labels.replace(to_replace='None', value=np.nan).dropna()

    # 限定超出边界值
    labels = max_min_limit(labels)

    # 导出处理之后的数据
    labels.to_csv(labelOutDataPath, encoding='utf-8', header=True, index=False, sep=",")

    # 生成单个标签文件
    out_label_folder = outLabelFolder
    if os.path.exists(out_label_folder) is False:
        os.makedirs(out_label_folder, exist_ok=False)
    save_labels(out_label_folder, labels)

    # 生成图片uri文件
    out_uri = outUriFolder
    if os.path.exists(out_uri) is False:
        os.makedirs(out_uri, exist_ok=False)
    save_all_image_uri(out_uri, labels)