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
    # 9: 2,
    # 13: 3,
    11: 2
}

# class_map = {
#     37:  0,
#     76:  1,
#     36:  2,
#     1:   3,
#     5:   4,
#     100: 5,
#     6:   6,
#     35:  7,
#     3:   8,
#     4:   9,
#     999: 10
# }


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
        # return class_map.get(map_key)
        return class_map.get(int(classId))
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
    overlapping_boxes = 0
    invalid_boxes = 0
    for name, group in grouped:
        fileName = label_path + "/{}.txt".format(name)
        out = group[['class_code', 'coordinate_x', 'coordinate_y', 'width', 'height']]
        out1 = remove_invalid_boxes(out.copy())
        if out.shape[0] != out1.shape[0]:
            invalid_boxes += out.shape[0] - out1.shape[0]
        out2 = remove_overlapping_boxes(out1.copy())
        if out1.shape[0] != out2.shape[0]:
            overlapping_boxes += out.shape[0] - out2.shape[0]
        print("total: {}, overlapping_boxes: {} ,remove_invalid_boxes: {}".format(out.shape[0],  out.shape[0] - out2.shape[0], out.shape[0] - out1.shape[0]))
        out.to_csv(fileName, encoding='utf-8', header=False, index=False, sep=" ")
    print("total: {}, overlapping_boxes: {} ,remove_invalid_boxes: {}".format(grouped.ngroups, overlapping_boxes, invalid_boxes))

def remove_invalid_boxes(boxes, min_aspect_ratio=1/3, max_aspect_ratio=3):
    """
    去除长宽比不合适的标注框

    Args:
        boxes: pandas DataFrame，包含标注框信息
        min_aspect_ratio: float，最小长宽比，默认为0.5
        max_aspect_ratio: float，最大长宽比，默认为2.0

    Returns:
        pandas DataFrame，去除长宽比不合适的标注框信息
    """
    # 计算标注框的长宽比
    aspect_ratio = boxes['width'] / boxes['height']

    # 筛选符合要求的标注框
    valid_boxes = boxes[(aspect_ratio >= min_aspect_ratio) & (aspect_ratio <= max_aspect_ratio)]
    # in_valid_boxes = boxes[(aspect_ratio < min_aspect_ratio) | (aspect_ratio > max_aspect_ratio)]
    # if in_valid_boxes.shape[0] > 0:
    #    print("")
    return valid_boxes

def calculate_iou(box1, boxes):
    """
    计算一个标注框与一组标注框的IOU

    Args:
        box1: pandas Series，标注框1
        boxes: pandas DataFrame，包含一组标注框

    Returns:
        numpy ndarray，IOU数组
    """
    # 计算box1的面积
    area1 = box1['width'] * box1['height']

    # 计算boxes的面积
    area2 = boxes['width'] * boxes['height']

    # 计算交集框的坐标
    x1 = np.maximum(box1['coordinate_x'], boxes['coordinate_x'])
    y1 = np.maximum(box1['coordinate_y'], boxes['coordinate_y'])
    x2 = np.minimum(box1['coordinate_x'] + box1['width'], boxes['coordinate_x'] + boxes['width'])
    y2 = np.minimum(box1['coordinate_y'] + box1['height'], boxes['coordinate_y'] + boxes['height'])

    # 计算交集框的面积
    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)

    # 计算IOU
    iou = intersection / (area1 + area2 - intersection)

    return iou.values

def remove_overlapping_boxes(boxes, IOU_THRESHOLD=0.9):
    """
    去除重叠的标注框

    Args:
        boxes: pandas DataFrame，包含标注框信息

    Returns:
        pandas DataFrame，去除重叠框后的标注框信息
    """
    # 根据标注框左上角坐标计算右下角坐标
    boxes['x2'] = boxes['coordinate_x'] + boxes['width']
    boxes['y2'] = boxes['coordinate_y'] + boxes['height']

    # 按照标注框类别分组
    grouped = boxes.groupby('class_code')

    # 去除重叠框
    new_boxes = []
    for name, group in grouped:
        while len(group) > 0:
            # 取出第一个标注框，将其加入新标注框列表
            new_boxes.append(group.iloc[0])

            # 计算第一个标注框和其余标注框的IOU
            ious = calculate_iou(group.iloc[0], group.iloc[1:])

            # 找到IOU小于阈值的标注框
            overlapping_boxes = group.iloc[1:][ious < IOU_THRESHOLD]

            # 更新group，继续迭代
            group = overlapping_boxes

    # 将新标注框列表转换为DataFrame
    new_boxes = pd.DataFrame(new_boxes)[['class_code', 'coordinate_x', 'coordinate_y', 'width', 'height']]

    return new_boxes


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


    # class_map = read_label_map(labelConfigPath)
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