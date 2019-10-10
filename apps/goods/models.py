from django.db import models
from tinymce.models import HTMLField   # 导入富文本标签的属性HTMLField
from db.base_model import BaseModel
# Create your models here.

class GoodsType(BaseModel):
    '''商品类型模型类'''
    name = models.CharField(max_length=20,verbose_name='种类名称')
    # 之所以logo用字符类型不用图片类型，因为前端代码用的class='xxx'，根据xxx指向不同的图片
    logo = models.CharField(max_length=20,verbose_name='标识')
    # upload_to类型是自定义图片上传的路径
    image = models.ImageField(upload_to='type',verbose_name='商品类型图片')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSKU(BaseModel):
    '''商品SKU模型类'''
    status_choices = (
        (0,'下线'),
        (1,'上线')
    )
    type = models.ForeignKey('GoodsType',verbose_name='商品类型',on_delete=models.CASCADE)
    goods = models.ForeignKey('Goods',verbose_name='商品SPU',on_delete=models.CASCADE)
    name = models.CharField(max_length=20,verbose_name='商品名称')
    desc = models.CharField(max_length=256,verbose_name='商品简介')
    # decimal_places是小数点保留位数
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    unite = models.CharField(max_length=20,verbose_name='商品单位')
    image = models.ImageField(upload_to='goods',verbose_name='商品图片')
    stock = models.IntegerField(default=1,verbose_name='商品库存')
    sales = models.IntegerField(default=0,verbose_name='商品销量')
    # choices 可以用来限定它的取值，你自己定义一个元组
    status = models.SmallIntegerField(default=1,choices=status_choices,verbose_name='商品状态')

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品(SKU)'
        verbose_name_plural = verbose_name

class Goods(BaseModel):
    '''商品SPU模型类'''
    name = models.CharField(max_length=20,verbose_name='商品SPU名称')
    # HTMLField不是我们django的类型，是我们引入的富文本的类型（即带有格式的文本）
    detail = HTMLField(blank=True,verbose_name='商品详情')

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品(SPU)'
        verbose_name_plural = verbose_name


class GoodsImage(BaseModel):
    '''商品图片模型类'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods',verbose_name='图片路径')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    '''首页轮播商品展示模型类'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner',verbose_name='图片') # 我们压根不用这个django自带的文件存储系统，upload_to参数随便写
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name


class IndexTypeGoodsBanner(BaseModel):
    '''首页分类商品展示模型类'''
    DISPLAY_TYPE_CHOICES = (
        (0, '标题'),
        (1, '图片')
    )
    type = models.ForeignKey('GoodsType',verbose_name='商品类型',on_delete=models.CASCADE)
    sku = models.ForeignKey('GoodsSKU',verbose_name='商品SKU',on_delete=models.CASCADE)
    display_type = models.SmallIntegerField(default=1,choices=DISPLAY_TYPE_CHOICES,verbose_name='展示类型')
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = '主要分类展示商品'
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    '''首页促销活动模型类'''
    name = models.CharField(max_length=20,verbose_name='活动名称')
    url = models.URLField(verbose_name='活动链接')
    image = models.ImageField(upload_to='banner',verbose_name='活动图片')
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = '主页促销活动'
        verbose_name_plural = verbose_name




