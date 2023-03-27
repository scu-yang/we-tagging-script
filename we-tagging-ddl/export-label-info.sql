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




select img_id,category_id,class_id,coordinate_x,coordinate_y,width,height,uri,md5 from image_label as lable join
(
select md5, id , uri from image_info as image  where image.version in ('血细胞图V1','外周血细胞数据集')
and image.label_num > 0
) as img
on lable.img_id  = img.id
where category_id  is not null
and class_id in (
37,76,36,1,5,100,6,35,3,4,
8,82,87
)

select category_id, category_name, class_id, class_name, class_code
from label_config where version = '血细胞标签集V1'
and class_id in (
37,76,36,1,5,100,6,35,3,4,
8,82,87
)