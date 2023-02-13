-- 给类别编码
set @r:=-1;
UPDATE label_config  SET class_code=(@r:=@r+1) where version = '类器官标签集V1' order by class_id  asc;

-- 导出已经打标签的图片和标签
select img_id,category_id,class_id,coordinate_x,coordinate_y,width,height,uri,md5 from image_label as lable join
(
select md5, id , uri from image_info as image  where image.version = '类器官数据' and image.label_num > 0
) as img
on lable.img_id  = img.id
where category_id  is not null
;


-- 导出标签配置
select category_id, category_name, class_id, class_name, class_code
from label_config where version = '类器官标签集V1'


select img_id,category_id,class_id,
CASE class_id
           WHEN 5 THEN 5
           WHEN 7 THEN 7
            WHEN 13 THEN 7
           ELSE class_id
       END AS class_id,

coordinate_x,coordinate_y,width,height,uri,md5 from image_label as lable join
(
select md5, id , uri from image_info as image  where image.version = '类器官数据' and image.label_num > 0
) as img
on lable.img_id  = img.id
where category_id  is not null
and  class_id in (5, 7, 13)


