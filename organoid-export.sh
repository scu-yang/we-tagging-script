#!/bin/bash

rootFolder=organoid-label-export-221115

python label.py \
-c organoid-label-export/organoid_config_202210091320.csv \
-d ${rootFolder}/organoid_label_202211152203.csv \
-o ${rootFolder}/organoid_label_out_202211152203.csv \
-i ${rootFolder}/out-uri \
-l ${rootFolder}/out-labels


python export_images.py \
-o ${rootFolder}/out-images \
-f ${rootFolder}/out-uri/uri.txt

python split-data-set.py \
-l ${rootFolder}/out-labels \
-i ${rootFolder}/out-images \
-o ${rootFolder}/data-set

cd ${rootFolder}
zip -9 -r out.zip data-set
