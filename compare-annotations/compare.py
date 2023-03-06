import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def read_yolo_annotation_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    annotations = []
    for line in lines:
        parts = line.strip().split()
        category_id = int(parts[0])
        bbox_center_x = float(parts[1])
        bbox_center_y = float(parts[2])
        bbox_width = float(parts[3])
        bbox_height = float(parts[4])
        x1 = bbox_center_x - bbox_width / 2
        y1 = bbox_center_y - bbox_height / 2
        x2 = bbox_center_x + bbox_width / 2
        y2 = bbox_center_y + bbox_height / 2
        annotation = {
            'class': category_id,
            'bbox': [x1, y1, x2, y2],
        }
        annotations.append(annotation)
    return annotations


def filter_annotations_with_low_similarity(annotations, predictions, iou_threshold=0.4, accuracy_threshold=0.4):
    filtered_annotations = []
    # 比较IOU和类别后, 对不上的部分
    no_filt = []
    for ann in annotations:
        gt_bbox = ann['bbox']
        gt_class = ann['class']
        iou_scores = []
        acc_scores = []
        for pred in predictions:
            pred_bbox = pred['bbox']
            pred_class = pred['class']
            iou = calculate_iou(gt_bbox, pred_bbox)
            iou_scores.append(iou)
            if pred_class == gt_class:
                acc_scores.append(1)
            else:
                acc_scores.append(0)
        max_iou = np.max(iou_scores)
        max_acc = np.max(acc_scores)
        if max_iou >= iou_threshold and max_acc >= accuracy_threshold:
            filtered_annotations.append(ann)
        else:
            no_filt.append(ann)

    # 去掉原始数据集中重复的框
    temp = annotations + no_filt
    overlapping_boxes = remove_overlapping_boxes(temp)
    aspect_ratio = check_aspect_ratio(annotations)
    print("长宽比不合适的数量: %s" % len(aspect_ratio)
          , "重叠的框和预测集对不上的框: %s" % len(overlapping_boxes))
    return filtered_annotations, overlapping_boxes + aspect_ratio


def check_aspect_ratio(bboxes, aspect_ratio_range=(0.33, 3)):
    """Check the aspect ratio of bounding boxes"""
    problematic_bboxes = []
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox['bbox']
        w = x2 - x1
        h = y2 - y1
        aspect_ratio = w / h
        if aspect_ratio < aspect_ratio_range[0] or aspect_ratio > aspect_ratio_range[1]:
            problematic_bboxes.append(bbox)
    return problematic_bboxes

def remove_overlapping_boxes(annotations, iou_threshold=0.9):
    new_annotations = []
    for i in range(len(annotations)):
        box1 = annotations[i]['bbox']
        for j in range(i+1, len(annotations)):
            box2 = annotations[j]['bbox']
            iou = calculate_iou(box1, box2)
            if iou > iou_threshold:
                if annotations[i]['class'] == annotations[j]['class']:
                    if annotations[i]['bbox'][2]*annotations[i]['bbox'][3] > annotations[j]['bbox'][2]*annotations[j]['bbox'][3]:
                        # annotations.pop(j)
                        new_annotations.append(annotations[j])
                    else:
                        # annotations.pop(i)
                        new_annotations.append(annotations[i])
                    break
    return new_annotations

def calculate_iou(bbox1, bbox2):
    x1, y1, w1, h1 = bbox1
    x2, y2, w2, h2 = bbox2
    xA = max(x1, x2)
    yA = max(y1, y2)
    xB = min(x1 + w1, x2 + w2)
    yB = min(y1 + h1, y2 + h2)
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = w1 * h1
    boxBArea = w2 * h2
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def plot_image(image_path, annotations, title=None):
    image = Image.open(image_path)
    # 绘制边界框
    fig, ax = plt.subplots(1)
    ax.imshow(image)
    w,h = image.size
    for ann in annotations:
        category_id = ann['class']
        bbox = ann['bbox']
        x1, y1, x2, y2 = bbox
        x1, y1, x2, y2 = x1*w, y1*h, x2*w, y2*h
        rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(x1, y1 - 5, str(category_id), fontsize=12, color='r')
    plt.title(title, loc="left")
    # 显示图片
    plt.show()

def plot_images(image_path, annotations, predictions, ans, no_ans, title = None, isShow=False):
    image = Image.open(image_path)
    fig, axs = plt.subplots(2, 2, figsize=(24, 20), sharex=True, sharey=True)
    get_plot(axs[0][0], image, annotations, "标注结果")
    get_plot(axs[0][1], image, no_ans, "过滤掉的标注集标签")
    get_plot(axs[1][0], image, predictions, "预测结果")
    get_plot(axs[1][1], image, ans, "过滤后的标注集标签")
    fig.tight_layout()
    if isShow:
        plt.show()
    return plt

def get_plot(axs,image, data, title=None, colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']):
    w, h = image.size
    axs.set_title(title)
    axs.imshow(image)
    for ann in data:
        category_id = ann['class']
        bbox = ann['bbox']
        x1, y1, x2, y2 = bbox
        x1, y1, x2, y2 = x1 * w, y1 * h, x2 * w, y2 * h
        color = colors[category_id % len(colors)]
        rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor=color, facecolor='none')
        axs.add_patch(rect)
        axs.text(x1, y1 - 5, str(category_id), fontsize=8, color=color)

def compare_single_file(file):
    file_name = file.split(".")[0]
    annotations = read_yolo_annotation_file("data/labels/{}.txt".format(file_name))
    predictions = read_yolo_annotation_file("data/var/labels/{}.txt".format(file_name))
    ans, no_ans= filter_annotations_with_low_similarity(annotations, predictions)
    # plot_image("data/var/images/{}.jpg".format(name), ans, "ans")
    plt = plot_images("data/var/images/{}".format(file), annotations, predictions, ans, no_ans, file)
    plt.savefig("result/{}".format(file_name))
    plt.close()


if __name__ == '__main__':
    files = os.listdir("data/var/images")

    # 单进程单线程
    # for index,file in enumerate(files):
    #     compare_single_file(file)
    #     print("完成 %s %, index: %s, file: %s" % (1.0*index/len(files), index, file))
    # print("end")

    # 多进程
    import concurrent.futures
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(compare_single_file, file) for file in files]
    concurrent.futures.wait(futures)
    print("end")