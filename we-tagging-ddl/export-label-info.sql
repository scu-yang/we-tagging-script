-- 给类别编码
set @r:=-1;
UPDATE label_config  SET class_code=(@r:=@r+1) where version = '血细胞标签集V1' order by category_id asc;

-- 导出血液细胞已经打标签的图片和标签
select img_id,category_id,class_id,coordinate_x,coordinate_y,width,height,uri,md5 from image_label as lable join
(
select md5, id , uri from image_info as image  where image.version = '血细胞图V1' and image.label_num > 0
) as img
on lable.img_id  = img.id
where category_id  is not null
;

-- 导出血液细胞已经打标签的图片和标签（无标签的框也导出）
select img_id,category_id,class_id,coordinate_x,coordinate_y,width,height,uri,md5 from image_label as lable join
(
select md5, id , uri from image_info as image  where image.version = '血细胞图V1' and image.label_num > 0
) as img
on lable.img_id  = img.id
;

-- 导出血液细胞标签配置
select category_id, category_name, class_id, class_name, class_code
from label_config where version = '血细胞标签集V1'

