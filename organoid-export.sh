#!/bin/bash

python label.py -c organoid-label-export/organoid_config_202210091320.csv \
-d organoid-label-export-221115/organoid_label_202211152203.csv \
-o organoid-label-export-221115/organoid_label_out_202211152203.csv \
-i organoid-label-export-221115/out-uri \
-l organoid-label-export-221115/out-labels


python export_images.py -o organoid-label-export-221115/out-images \
-f organoid-label-export-221115/out-uri/uri.txt

python split-data-set.py -l organoid-label-export-221115/out-labels \
-i organoid-label-export-221115/out-images \
-o organoid-label-export-221115/data-set

cd organoid-label-export-221115
zip -9 -r out.zip data-set
