import pandas as pd
import os
class_map = {
    5: 0,
    7: 1,
    9: 2,
    13: 3,
    11: 4
}

def transfer_label_class(data: pd.DataFrame) -> pd.DataFrame:
    data["class_id"] = data["class_id"].replace(class_map)
    return data

def save_labels(data: pd.DataFrame)->None:
    grouped = data.groupby('md5')

    for name, group in grouped:
        fileName = "label/labels/{}.txt".format(name)
        out = group[['class_id', 'coordinate_x', 'coordinate_y', 'width', 'height']]
        out.to_csv(fileName, encoding='utf-8', header=False, index=False,sep=" " )

def save_all_image_uri(folder, data: pd.DataFrame) -> None:
    uri = data['uri'].unique()
    with open(folder + "/uri.txt", 'w') as f:
        for item in uri:
            f.write(item)
            f.write("\n")

def read_label_map(config_path: str)->dict:
    config = pd.read_csv(config_path, encoding='utf-8')
    result = {}
    for row in config.iterrows():
        categoryId = row[1]['category_id']
        classId = row[1]['class_id']
        className = row[1]['class_name']
        classCode = row[1]['class_code']
        if className is '-':
            classId = 'None'
        map_key = "{}:{}".format(categoryId, classId)
        result[map_key] = classCode
    return result

if __name__ == '__main__':
    labels = pd.read_csv("blood-cells-label-export/react_only_label_202210081652.csv", encoding='utf-8')
    #labels = transfer_label_class(labels)
    #save_labels(labels)
    save_all_image_uri("blood-cells-label-export/out", labels)
    #config = read_label_map("blood-cells-label-export/label_config_202210081650.csv")
    pass