# 类器官数据

## 数据范围

1. 只包括正常类器官 data-set-1

```shell
# 导出

python label.py \ 
-c organoid-label-export\organoid_config_202210091320.csv \
-d organoid-label-export-230212\data-set-1.csv \
-o organoid-label-export-230212\label_file_out \



```

2. 包括正常类器官和模糊类器官, 识别为两类 data-set-2
3. 包括正常类器官, 变异的类器官，模糊类器官+模糊变异的类器官 data-set-3


