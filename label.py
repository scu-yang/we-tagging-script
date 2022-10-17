import numpy as np
import pandas as pd
import os

class_map = {
    5: 0,
    7: 1,
    9: 2,
    13: 3,
    11: 4
}


def transfer_label_class(data: pd.DataFrame, needTransfer=True) -> pd.DataFrame:
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


def max_min_limit(data: pd.DataFrame) -> pd.DataFrame:
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


def save_labels(label_path, data: pd.DataFrame) -> None:
    grouped = data.groupby('md5')

    for name, group in grouped:
        fileName = label_path + "/{}.txt".format(name)
        out = group[['class_code', 'coordinate_x', 'coordinate_y', 'width', 'height']]
        out.to_csv(fileName, encoding='utf-8', header=False, index=False, sep=" ")


def save_all_image_uri(folder, data: pd.DataFrame) -> None:
    uri = data['uri'].unique()
    with open(folder + "/uri.txt", 'w') as f:
        for item in uri:
            f.write(item)
            f.write("\n")


def read_label_map(config_path: str) -> dict:
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
    class_map = read_label_map("blood-cells-label-export/label_config_202210081650.csv")

    labels = pd.read_csv("blood-lzj-221017/first-clean.csv"
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
    #labels = transfer_label_class(labels)
    # labels = labels.replace(to_replace='None', value=np.nan).dropna()

    # 限定超出边界值
    #labels = max_min_limit(labels)

    # 导出处理之后的数据
    #labels.to_csv("blood-lzj-221017/out-label.csv", encoding='utf-8', header=True, index=False, sep=",")

    # 生成单个标签文件
    out_label_folder = "blood-lzj-221017/out-labels"
    if os.path.exists(out_label_folder) is False:
        os.makedirs(out_label_folder, exist_ok=False)
    save_labels(out_label_folder, labels)

    # 生成图片uri文件
    out_uri = "blood-lzj-221017/out"
    if os.path.exists(out_uri) is False:
        os.makedirs(out_uri, exist_ok=False)
    save_all_image_uri(out_uri, labels)

