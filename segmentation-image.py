import argparse
import cv2
import numpy as np
import pandas as pd
import os

__version__ = "2022.10.08"

def version():
    return "version:" + __version__


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
parser.add_argument('-l', '--labelPath', type=str, default="seg-img/out-label.csv", help='Label file path')
parser.add_argument('-o', '--outPath', type=str, default="seg-img/out", help='Label file path')
parser.add_argument('-r', '--imageRoot', type=str, default="/home/image_root/ossRoot/", help='Image root path')
parser.add_argument('-d', '--drawSeg', type=bool, default=False, help='Label file path')
parser.add_argument('-s', '--drawSegOut', type=str, default="seg-img/seg-out", help='Label file path')

args = parser.parse_args()

classCodeMap: dict = {
    "68": '巨（中性）晚幼粒细胞',
    "67": '巨（中性）杆状核粒细胞',
    "56": "中性晚幼粒细胞",
    "57": "中性杆状核粒细胞",
    "58": '中性分叶核粒细胞',
    "92": '成熟淋巴细胞',
    "2": '中幼红细胞',
    "3": '晚幼红细胞',
    "23": "泪滴形红细胞",
    "139": "巨/大血小板",
    "140": "血小板聚集",
    "141": "正常血小板",
    "142": "小血小板",
    "148": "血小板卫星现象",
    "149": "颗粒减少的血小板",
    "150": "畸形血小板",
    "59": "嗜酸性中幼粒细胞",
    "60": "嗜酸性晚幼粒细胞",
    '63': "嗜碱性中幼粒细胞",
    '64': '嗜碱性晚幼粒细胞',
    '4': '成熟红细胞',
    # '38': '红细胞系',
    '103': '单核细胞',
    "23": '泪滴形红细胞'
}

classCodeMapKeys = classCodeMap.keys();


def open_image(imagePath: str, labels: pd.DataFrame):
    img = cv2.imread(imagePath)
    draw = cv2.imread(imagePath)
    if img is None or img.shape == 0:
        print("cannot find image at path: {}".format(imagePath))
        return
    print("img path: {}, shape: {}".format(imagePath, img.shape))
    imgH = img.shape[0]
    imgW = img.shape[1]
    for row in labels.itertuples():
        classCode = getattr(row, 'class_id')
        if str(classCode) not in classCodeMapKeys:
            continue
        imgId = getattr(row, 'img_id')
        x = getattr(row, 'coordinate_x')
        y = getattr(row, 'coordinate_y')
        w = getattr(row, 'width')
        h = getattr(row, 'height')
        realW = w * imgW
        realH = h * imgH
        startX = max(0, int(x * imgW - realW / 2))
        endX = min(imgW, int(x * imgW + realW / 2))
        startY = max(0, int(y * imgH - realH / 2))
        endY = min(imgH, int(y * imgH + realH / 2))
        if endY - startY <=1 or endX-startX<=1:
            continue
        crop = img[startY:endY, startX:endX]
        if crop is None or crop.shape == 0:
            print("{} crop: {}-{}-{}-{}".format(imagePath, startY,endY, startX,endX))
            continue

        classObjFolder = "{}/{}".format(args.outPath, classCode)
        if os.path.exists(classObjFolder) is False:
            os.makedirs(classObjFolder, exist_ok=False)
        name = "{}_{}_{}_{}".format(imgId, classCode, x, y)
        cv2.imwrite(classObjFolder + "/" + name+'.jpg', crop)
        if args.drawSeg:
            ptLeftTop = (startX, startY)
            ptRightBottom = (endX, endY)
            point_color = (0, 0, 255)  # BGR
            thickness = 1
            lineType = 8
            cv2.rectangle(draw, ptLeftTop, ptRightBottom, point_color, thickness, lineType)
    if args.drawSeg:
        cv2.imwrite(os.path.join(args.drawSegOut, str(imgId), '.jpg'), draw)
        if os.path.exists(args.drawSegOut) is False:
            os.makedirs(args.drawSegOut, exist_ok=False)
        # cv2.namedWindow("AlanWang")
        # cv2.imshow('AlanWang', draw)
        # cv2.waitKey(30000)  # 显示 10000 ms 即 10s 后消失
        # cv2.destroyAllWindows()


if __name__ == '__main__':
    labelPath = args.labelPath
    labels = pd.read_csv(labelPath
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
                                  # "class_code": str
                                  }
                         )
    grouped = labels.groupby('uri')
    index = 0
    for uri, group in grouped:
        out = group[['img_id', 'class_code', 'coordinate_x', 'coordinate_y', 'width', 'height']]
        imagePath: str = (args.imageRoot + uri).replace(u"//", '/').replace(u"//", '/')
        open_image(imagePath, out)
        index+=1
        if index % 20 == 0:
            print("{}-{}", index, grouped.size)