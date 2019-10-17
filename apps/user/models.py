from django.db import models
from django.contrib.auth.models import AbstractUser # 这个是验证模块，导入过来去继承他
from db.base_model import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import  settings
# Create your models here.

# 使用django内置的应用系统，即AbstractUser类，我们继承这个类就可以直接用
# 所以我们这什么字段都没有定义，没必要，迁移会自动帮我们生成user表
class User(AbstractUser,BaseModel):
    '''用户模型类（继承这两个类，后面一个类是我们自己写的）'''
    def generate_active_token(self):
        '''生成用户签名字符串'''
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':self.id}
        token = serializer.dumps(info)
        return token.decode()

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        # verbose_name_plural的作用是本来显示’用户s‘，去掉s字符
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    '''地址模型管理器类'''
    # 定义模型管理器类的应用场景有两个
    # 1、改变原有的查询结果集:all()    即user.objects.all()
    # 2、封装方法：用户操作模型类对应的数据表（增删改查）

    def get_default_address(self, user):
        '''获取用户的默认收货地址'''
        # try:
        #     address = Address.objects.get(user=user, is_default=True) #  objects是models.manager管理类的对象
        # except Address.DoesNotExist:
        #     address = None
        # 因为self.model属性可以获取self对象所在的模型类，所以我们写成self.model.objects.get(user=user, is_default=True),但是self.model就是objects,明显重复了
        try:
            address = self.get(user=user, is_default=True) #  objects是models.manager管理类的对象
        except self.model.DoesNotExist:  # 查不到默认收货地址会抛出DoesNotExist
            #  不存在默认收货地址
            address = None
        return  address


class Address(BaseModel):
    '''地址模型类'''
    user= models.ForeignKey('User',verbose_name='所属账户',on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20,verbose_name='收件人')
    addr = models.CharField(max_length=256,verbose_name='收件地址')
    zip_code = models.CharField(max_length=6,null=True,verbose_name='邮政编码')
    phone = models.CharField(max_length=11,verbose_name='联系电话')
    is_default= models.BooleanField(default=False,verbose_name='是否默认')

    # 自定义一个模型管理器的对象,原来的objects.all()中的objects成了我们定义的
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name