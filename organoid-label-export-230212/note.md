# 类器官数据

## 数据范围

1. 只包括正常类器官 data-set-1

```shell
# 导出

python label.py -c organoid-label-export/organoid_config_202210091320.csv -d organoid-label-export-230212/data-set-1.csv -o organoid-label-export-230212/label_file_out -i organoid-label-export-230212/out-uri -l organoid-label-export-230212/out-labels

python3 train.py --workers 8 --device 0 --batch-size 32 \
--data /home/pengdie/loorr-temp/20230212-data-set-1/data.yaml --img 640 640 --cfg cfg/training/yolov7-data-set-1.yaml \
--weights '' --name yolov7-data-set-1 --hyp data/hyp.scratch.p5.yaml
```
2. 包括正常类器官, 模糊类器官+模糊变异的类器官 data-set-2
3. 包括正常类器官和模糊类器官, 识别为两类 data-set-3
4. 包括正常类器官, 变异的类器官，模糊类器官+模糊变异的类器官 data-set-4


train: /home/pengdie/loorr-temp/20230212-data-set-1/train/images
val: /home/pengdie/loorr-temp/20230212-data-set-1/test/images

nc: 1
names: ['1']