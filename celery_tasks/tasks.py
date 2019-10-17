# coding=UTF-8
import time
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader, RequestContext

# 在任务处理者中开启 Django项目运行配置
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_dailyfresh.settings")
django.setup()

from goods.models import GoodsType, IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner

# 创建一个Celery类的实例对象，第一个参数一般写要异步处理代码的文件，第二个是你的redis数据库，使用8号库
app = Celery('celery_tasks.tasks',broker='redis://192.168.31.131:6379/8')

# 定义任务函数
# 这里必须要用Celery类的实例方法task来装饰我们定义的发送邮件的函数
@app.task
def send_register_active_email(email, username, token):
    """发送激活邮件"""
    # 组织邮件信息
    subject = '天天生鲜欢迎信息'
    message = ''
    html_message = '<h1>{0},欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/{1}">http://127.0.0.1:8000/user/active/{2}</a>'.format(
    username, token, token)
    sender = settings.EMAIL_FROM  # 发件人是谁，我们settings文件中的邮箱配置中的参数
    receiver = [email]

    # 如果用message属性来接受的话发过去的就是纯字符串，我们这里有可以点击的链接，所以用html_messagedend_mail方法的参数
    # send_mail函数是把邮件发送到smtp服务器，由smtp服务器再转发给目的邮箱
    # send_mail函数前面四个参数是按顺序传的，可以直接写上数据，当然你也可以显式的去指定，但是html_message没有顺序，你必须指定该属性
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(6)  # 模拟一下，你看着是6秒，但是用了异步，秒跳转到登陆页面
    # 而这个 send_mail 函数是阻塞型的，他要等smtp服务器发给用户之后才会继续执行下面的代码，造成用户不好的体验，我都等了5到6秒菜跳转到首页

    # 当项目里面出现这种或者比较耗时的操作，你就可以用django的celery(异步处理第三方库：我交给你了我就不管了，我继续执行我的代码，你自己去干我交给你的事)
    # 即我们把这个发邮件功能的代码单独放到一个python包中，作为异步处理的代码

# 用定义的任务函数.delay(),发起任务！！！！！！！！！！
# 再celery上   celery -A celery_tasks.tasks worker -l info就能查看
@app.task
def generate_static_index_html():
    """产生首页静态页面"""
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners

    # 组织模板上下文
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners}

    # 使用模板
    # 1.加载模板文件,返回模板对象temp
    temp = loader.get_template('static_index.html')
    # 2.定义模板上下文
    # context = RequestContext(request, context)
    # 3.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应的静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')

    with open(save_path, 'w') as f:
        f.write(static_index_html)
