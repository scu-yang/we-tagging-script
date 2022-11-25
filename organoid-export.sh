#!/bin/bash

rootFolder=organoid-label-export-221125
labelName=or_train_and_var_202211252258
filePofix=.csv
fileFullName=${labelName}${filePofix}

echo "rootFolder: "${rootFolder}
echo "fileFullName: "${fileFullName}

python label.py \
-c organoid-label-export-2211125/organoid_config_202210091320.csv \
-d ${rootFolder}/${fileFullName} \
-o ${rootFolder}/out_${fileFullName} \
-i ${rootFolder}/out-uri \
-l ${rootFolder}/out-labels

python export_images.py \
-o ${rootFolder}/out-images \
-f ${rootFolder}/out-uri/uri.txt

python split-data-set.py \
-t 0.8 -e 0 -a 0.2 \
-l ${rootFolder}/out-labels \
-i ${rootFolder}/out-images \
-o ${rootFolder}/data-set

#cd ${rootFolder}
#zip -9 -r out.zip data-set
