from django.db import  models

# 我们定义一个继承于models.Model类的BaseModel类是为了给每一个模型类中增加这三个字段

class BaseModel(models.Model):
    '''模型抽象基类'''
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_delete = models.BooleanField(default=False,verbose_name='删除标记')

    # 记住如果你要这样的话一定要在元类中指定abstract = True，不然会报错
    class Meta:
        # 说明是一个抽象模型类
        abstract = True
