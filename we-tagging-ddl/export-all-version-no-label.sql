select img_id,category_id,class_id,coordinate_x,coordinate_y,width,height,uri,md5 from image_label as lable join
(
select md5, id , uri from image_info as image  where image.version in ('血细胞图V1', 'red_cell_1', '类器官数据') and image.label_num > 0
) as img
on lable.img_id  = img.id
where category_id  is not null
;

