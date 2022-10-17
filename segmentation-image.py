import argparse
import cv2
import numpy as np
import pandas as pd
import os

__version__ = "2022.10.08"

from tqdm import tqdm


def version():
    return "version:" + __version__


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=version(), help='Display version')
parser.add_argument('-l', '--labelPath', type=str, default="blood-cells-label-export/out-label.csv", help='Label file path')
parser.add_argument('-o', '--outPath', type=str, default="seg-img/out", help='Label file path')
parser.add_argument('-r', '--imageRoot', type=str, default="/home/image_root/ossRoot/", help='Image root path')
parser.add_argument('-d', '--drawSeg', type=bool, default=False, help='Label file path')
parser.add_argument('-s', '--drawSegOut', type=str, default="seg-img/seg-out", help='Label file path')

args = parser.parse_args()


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
        classCode = getattr(row, 'class_code')
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
        crop = img[startY:endY, startX:endX]

        name = "{}_{}_{}_{}".format(imgId, classCode, x, y)
        cv2.imwrite(os.path.join(args.outPath, name, '.jpg'), crop)
        if os.path.exists(args.outPath) is False:
            os.makedirs(args.outPath, exist_ok=False)
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
                                  "md5": str})
    grouped = labels.groupby('uri')
    for uri, group in grouped:
        out = group[['img_id', 'class_code', 'coordinate_x', 'coordinate_y', 'width', 'height']]
        imagePath: str = (args.imageRoot + uri).replace(u"//", '/').replace(u"//", '/')
        open_image(imagePath, out)
