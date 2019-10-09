from django.shortcuts import render,redirect  # 视图返回包和反向解析包
from django.core.urlresolvers import reverse
from django.core.mail import send_mail # django自带的发邮件包
from django.contrib.auth import authenticate, login, logout # 认证系统，authenticate认证一组给定用户名和密码，如果匹配返回User对象，否则返回None
from django.views.generic import View # 使用类试图，一个类中有多个方法，适用于多个功能用一个url地址
from django.http import HttpResponse
from django.conf import settings # 导入django的setting文件，比如后面使用的加密包的密钥，这个密钥可以不用这个自己设置一个
from goods.models import GoodsSKU
from user.models import User,Address

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer# 加密包,还有加密时间设置功能
from itsdangerous import SignatureExpired # 导入解密时抛出的异常
from celery_tasks.tasks import send_register_active_email  # 我们定义的异步处理发邮件的函数
# 我们安装的django_redis包是一个一个可以使django支持redis cache/seesion后端的包，即要有它才能用redis来存储seesion
from django_redis import get_redis_connection # 这个函数是django-redis包中专门用来连接redis数据库的
from utils.mixin import LoginRequiredMixin
import  re
# Create your views here.

# 装饰器，禁止某些ip访问
# EXCLUDE_IPS = ['192.168.31.134']
# def decorator1(view_func):
#     def wrapper(request,*view_args,**view_kwargs):
#         user_ip = request.META['REMOTE_ADDR']
#         if user_ip in EXCLUDE_IPS:
#             return HttpResponse('<h1>Forbidden</h1>')
#         else:
#             return  view_func(request,*view_args,**view_kwargs)
#     return wrapper

'''整合为一个地址，显示页面和注册处理，登陆也是一样的'''
# 地址配置：/user/register
# 你是get就说明你要请求注册页面，你是post就说明你已经输入了你的信息表单传过来了，所以我就进行注册处理

# def register(request):
#     '''注册'''
#     if request.method == 'GET':  # 直接请求一个注册地址是GET方式
#         print(settings.STATICFILES_FINDERS)
#         return render(request,'register.html') # 返回注册页面
#
#     else:
#         # 业务开发的注册处理都是分四步，定死了的：
#         # 1、接收表单提交过来的数据
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#         # 2、进行数据校验
#         # 数据是否完整
#         if not all([username, password, email]):
#             return render(request, 'register.html', {'errmsg': '数据不完整'})
#         # 检验邮箱，if not 不满足正则
#         if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#         if allow != 'on':
#             return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#         # 当用户名重复django用户认证系统会报1062错误，不可能给用户这个页面吧
#         try:
#             user = User.objects.get(username=username)
#         # get方法是有且仅有返回一条信息，如果找不到与注册名同名的用户名，会抛出DoesNotExist
#         except User.DoesNotExist:
#             # 用户名不存在
#             user = None
#         # 我们在注册界面返回一个错误提示就可以了
#         if user:
#             # 用户名已存在
#             return render(request, 'register.html', {'errmsg': '用户名已存在'})
#
#         # 3、进行用户注册
#         # 直接使用django自带的用户认证系统，django已经封装好了create_user方法，直接用
#         user = User.objects.create_user(username, email, password)
#         # 还有django用户认证系统中的is_action默认是激活状态，我们要修改为非激活
#         user.is_active = 0
#         user.save()
#
#         # 4、返回应答，注册是后台的事，所以他没有前端页面返回，一般是跳转到首页，所以反向解析到首页
#         return redirect(reverse('goods:index'))
#
#
# def register_handle(request):
#     '''处理注册的表单提交过来的数据'''
#     # 业务开发的注册处理都是分四步，定死了的：
#     # 1、接收表单提交过来的数据
#     username = request.POST.get('user_name')
#     password = request.POST.get('pwd')
#     email = request.POST.get('email')
#     allow = request.POST.get('allow')
#     # 2、进行数据校验
#     # 数据是否完整
#     if not all([username, password, email]):
#         return render(request, 'register.html', {'errmsg': '数据不完整'})
#     # 检验邮箱，if not 不满足正则
#     if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#         return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#     if allow != 'on':
#         return render(request,'register.html',{'errmsg':'请同意协议'})
#
#     # 当用户名重复django用户认证系统会报1062错误，不可能给用户这个页面吧
#     try:
#         user = User.objects.get(username=username)
#     # get方法是有且仅有返回一条信息，如果找不到与注册名同名的用户名，会抛出DoesNotExist
#     except User.DoesNotExist:
#         # 用户名不存在
#         user = None
#     # 我们在注册界面返回一个错误提示就可以了
#     if user:
#         # 用户名已存在
#         return render(request, 'register.html', {'errmsg': '用户名已存在'})
#
#     # 3、进行用户注册
#     # 直接使用django自带的用户认证系统，django已经封装好了create_user方法，直接用
#     user = User.objects.create_user(username, email, password)
#     # 还有django用户认证系统中的is_action默认是激活状态，我们要修改为非激活
#     user.is_active = 0
#     user.save()
#
#     # 返回应答,跳转到首页,工作后项目经理会跟你说用反向解析具体跳转到那个页面
#     # 4、返回应答，注册是后台的事，所以他没有前端页面返回，一般是跳转到首页，所以反向解析到首页
#     return redirect(reverse('goods:index'))



# /user/register  用类视图，使用同一个地址，注册处理和显示注册页面靠请求方式区别
class RegisterView(View):
    '''注册及注册处理'''
# 注册和注册处理使用同一个地址，因为表单就是要提交到注册那个url来被后端get到，注册界面get，表单提交post，后面的登陆界面和登录校验也是，你请求登录界面get方法，表单提交过来就是post。
    def get(self,request):
        '''显示注册页面'''
        return render(request,'register.html')
    def post(self,request):
        '''进行注册处理'''
        # 业务开发的注册处理都是分四步，定死了的：
        # 1、接收表单提交过来的数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 2、进行数据校验
        # 数据是否完整
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 检验邮箱，if not 不满足正则
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 当用户名重复django用户认证系统会报1062错误，不可能给用户这个页面吧
        try:
            user = User.objects.get(username=username)
        # get方法是有且仅有返回一条信息，如果找不到与注册名同名的用户名，会抛出DoesNotExist
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        # 我们在注册界面返回一个错误提示就可以了
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 3、进行用户注册
        # 直接使用django自带的用户认证系统，django已经封装好了create_user方法，直接用
        user = User.objects.create_user(username, email, password)
        # 还有django用户认证系统中的is_action默认是激活状态，我们要修改为非激活
        user.is_active = 0
        user.save()

        # 发送激活邮件，里面是激活链接显示：http: // 127.0.0.1:8000/user/active/3
        # 但是要把这些激活链接中的信息加密处理，加密这个id号，比如是3

        # ！！！加密用户的身份信息，生成激活用户token
        serializer = Serializer(settings.SECRET_KEY, 3600)  # settings.SECRET_KEY密钥一般使用django的setting文件中的那个，但也可以自己写，我们设置3600秒后过期
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # 加密，这个加密包是加密成bytes数据显示在链接中，我可以解码成utf8，就没有b'....'了，更好看一点
        token = token.decode()


        # 发邮件，我们用的异步处理来发邮件，详情见celery_tasks.tasks,防止用户等待，这里我们只需要发出异步任务
        # 这个delay函数就可以把这个异步任务放入任务队列，这就是我们用app.task装饰的作用
        send_register_active_email.delay(email,username,token)  # tasks中封装好了


        # 然后我们在ubuntu上接受任务，当然Ubuntu上你得虚拟环境中也得有celery包,当然还要有redis包，celery后端是redis


        # 如果用message属性来接受的话发过去的就是纯字符串，我们这里有可以点击的链接，所以用html_messagedend_mail方法的参数
        # send_mail函数是把邮件发送到smtp服务器，由smtp服务器再转发给目的邮箱
        # send_mail函数前面四个参数是按顺序传的，可以直接写上数据，当然你也可以显式的去指定，但是html_message没有顺序，你必须指定该属性
        # 而这个 send_mail 函数是阻塞型的，他要等smtp服务器发给用户之后才会继续执行下面的代码，造成用户不好的体验，我都等了5到6秒菜跳转到首页

        # 当项目里面出现这种或者比较耗时的操作，你就可以用django的celery(异步处理第三方库：我交给你了我就不管了，我继续执行我的代码，你自己去干我交给你的事)
        # 即我们把这个发邮件功能的代码单独放到一个python包中，作为异步处理的代码

        # 4、返回应答，注册是后台的事，所以他没有前端页面返回，一般是跳转到首页，所以反向解析到首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''用户激活'''   # #(就是把激活id改为1)，但是为了用户安全必须涉及到加密，然后get到后解密
    def get(self,request,token):
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)
            # 获取激活用户的id
            user_id = info['confirm']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1  #  激活成功
            user.save()
            # 跳转到登陆页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            # 如果抛出这个异常证明激活链接已过期
            return HttpResponse('激活链接已过过期时间')

# 地址：/user/login
class LoginView(View):
    """登录及登录校验"""
    def get(self, request):
        """显示登陆页面"""
        # 判断是否记住了用户名
        if 'username' in request.COOKIES: # 如果有则获取，并且把checked选中
            username = request.COOKIES.get('username')
            checked = 'checked'
        else: # 没有的话就不选中checked，不记住用户名
            username = ''
            checked = ''
        # 使用模板,并把这两个参数传过去执行
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        """登录校验"""
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理：登录校验
        # User.objects.get(username=username,password=password) # 本来是该这样去看你get是否能查到
        user = authenticate(username=username, password=password) # 但是我们可以使用django自动完成认证校验，django内置认证系统
        if user is not None: # 没有找到匹配到返回None
            # 用户密码正确
            if user.is_active: # 我们的is_active值是0或1
                # 记录用户的登陆状态(django框架很多自带的功能)
                # 如果你认证了一个用户，可以使用login()函数,django的seesion框架将用户的ID保存在seesion中，造成读写项目开发中我们经常会使用到用户session信息，所以都会使用到redis来缓存用户session
                # 而这个login函数（也是django认证系统中的），就是当你通过authenticate认证成功了一个用户，你就可以通过login来登入该用户，第一个参数是HttpResponse对象，第二个是认证成功的用户
                login(request, user)
                '''为什么要获取登陆后所要跳转的地址next_url,因为你直接/user，即你还没有登录，login_required会给你跳到登录界面(settings里设置好了这个函数的默认跳转为登录页面的地址），然后你
                   跳转到登陆界面,这时当前的url你会发现有个next参数，用来控制下一个跳转地址。但是当你是通过/user/login直接进入登录页面而不是由/user因为未登录而跳转过去的，
                   这时当前的url后面就没有这个会拿不到next（跳转地址），我们这里要把第二种情况的默认跳转地址设置为跳转到首页，当然你也可以设置成跳转到想要的地址
                '''
                # 如果是直接/user/login进入就没有next参数，返回None，我们就默认跳转到首页，后面的reverse('goods:index'就是默认值
                next_url = request.GET.get('next',reverse('goods:index'))
                # 跳转到首页'goods:index'
                response = redirect(next_url) # 这个redirect返回的是HttpResponseRedirect类的一个对象，它是HttpResponse的子类，符合我们的视图函数的定义：必须返回HttpResponse对象或404

                # 判断是否需要记住用户名 拿到表提交的remember值
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 记住用户名，时间7天
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回应答
                return response

            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


# /user/logout
class LogoutView(View):
    def get(self,request):
        '''退出登录'''
        # 会清除用户的session信息
        logout(request)  # 也是用django内置系统logout函数

        # 跳转到首页
        return redirect(reverse('goods:index'))


# 这三个页面必须用户登录后才能访问，用内置认证系统login_required判断，如果用户已登录则正常进入，否则跳转到一个地址，我们要在settings文件中配置为跳转到登录页面
# 地址:/user
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):                # page='user'
        """显示用户中心信息页"""
        # django会给request对象添加一个属性 request.user
        # 如果用户未登录  ->  user是AnonymousesUser类的一个实例，返回False
        # 如果用户登录->user是User类的一个实例,返回True
        # request.user.is_authenticates()

        # 既然你的用户中心要显示，那么你就要，获取用户的个人信息在用户中心页面上显示出来
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户的浏览记录
        # from redis import StrictRedis
        # sr = StrictRedis(host='172.16.179.130',port='6379',db=2) # 当host=localhost,port ='6379',db=0时，可以简写为sr = StrictRedis()
        con = get_redis_connection('default')  # 这个default就是setting中配置好的redis数据库
        history_key = 'history_%d'%user.id

        # 获取用户最新浏览的5个商品的id
        sku_ids = con.lrange(history_key,0,4)

        # # 从mysql数据库中查询用户浏览的商品的具体信息
        # goods_li = GoodsSKU.objects.filter(id__in=sku_ids)   # filter查询方法返回一个查询集
        #
        # 遍历有序的获取用户浏览的历史商品信息
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        # 除了你给模板文件传递的模板变量之外，django框架会把request.user也传递给模板文件
        return  render(request,'user_center_info.html',{
                            'page':'user',
                            'address':address,
                            'goods_li':goods_li}) # user对象是直接用不用传，只要用户登录我们获取到了之后


# /user/order
class UserOrderView(LoginRequiredMixin,View):             # page='order'
    """用户中心---订单页"""
    def get(self,request):
        """显示"""
        # 获取用户的订单信息

        return  render(request,'user_center_order.html',{'page':'order'})


# 地址：/user/address  这里也是显示用户地址页和添加地址使用同一个地址，用类视图，用get和post请求方式来区分
class AddressView(LoginRequiredMixin,View):          # page='address'
    """用户中心---地址页"""
    def get(self, request):
        """显示"""
        # 获取登录用户的user对象
        user = request.user
        # 获取用户的默认收货地址,mysql中去查默认收货地址，这里代码和下面重复了，我们可以自定义地址模型管理器类，来拿默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True) #  objects是models.manager管理类的对象
        # except Address.DoesNotExist:
        #     address = None
        address = Address.objects.get_default_address(user) # 这个get_default_address是我们自己在模型类中定义的，有默认地址则返回，没有则返回None

        # 使用模板并把address参数传过去,至于page变量就是传去前端模板，当然肯定有父模板就是去父模板中来拿到这个变量，if endif目前显示哪个页面，哪个才被class装饰成红色
        return render(request, 'user_center_site.html',{'page':'address','address':address})

    def post(self,request):
        '''地址的添加'''
        # 1\接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        # 2\校验数据
        if not all([receiver,addr,phone]):   # 我们的user.models的zip_code属性设置为可以为空，所以邮编可以不用校验
            return render(request,'user_center_site.html',{'errmsg':'数据不完整'})
        # 手机号是否格式正确
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$',phone):
            return render(request,'user_center_site.html',{'errmsg':'手机格式不正确'})
        # 业务处理:地址添加
        # 如果用户有了收货地址，添加的地中不作为默认收货地址，否则就设为默认地址
        # 获取当前已经登录用户对应的用户user对象request.user，django框自带功能（用户认证系统auth里面的）
        user = request.user

        # try:
        #     address = Address.objects.get(user=user,is_default=True)
        # except Address.DoesNotExist:
        #     address = None
        address = Address.objects.get_default_address(user) # 这就是自定义管理器类的作用这行代码代替了前四行代码（自己在user的models里面去看）

        if address:
            is_default = False
        else:
            is_default = True
        # 添加地址
        Address.objects.create(user=user,
                           addr=addr,
                           receiver=receiver,
                           zip_code=zip_code,
                           phone=phone,
                           is_default=is_default)


        # 3\返回应答，刷新地址页面
        return redirect(reverse('user:address')) # get请求方式，所以又重定向到了get函数，返回user_center_site.html页面