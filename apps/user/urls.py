from django.conf.urls import url
from django.contrib.auth.decorators import login_required # 这是个django用户认证系统中的一个函数，我们项目中的三个页面：用户信息页，订单页，地址页那肯定是得登陆后才能访问，它是怎么来判断登陆与否。
# from user import views
from user.views import RegisterView, ActiveView, LoginView,UserInfoView,UserOrderView,AddressView,LogoutView

urlpatterns = [
    # as_view是类试图的意思，如果是方法不是类就可以.方法名，如果是类试图就要.as_view(),as_view方法会自动去匹配到底使用这个类试图中的那个类方法。
    # url(r'^register$',views.register,name='register'),# 显示注册页面
    # url(r'^register_handle$',views.register_handle,name='register_handle'),# 注册处理，前端表单提交过来
    url(r'^register$',RegisterView.as_view(),name='register'), # 显示住粗页面和注册处理使用这个一样的地址
    # 这个(?P<token>.*)是捕获地址中的加密信息，我们拿到类视图中的get方法中去解密处id来，再把这个id对应的is_active改为1
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'), # 激活
    url(r'^login$',LoginView.as_view(),name='login'), # 登录
    url(r'^logout$',LogoutView.as_view(),name='logout'), # 注销登录
    # 用户中心的3个页面,信息也订单页地页
    # 我们用login_required函数来包住类视图函数，就能自动帮我们去判断用户登录了没有，有则可以进去信息页，否则跳转到一个默认地址，我们要在settings文件中修改为跳转到登录页面

    # url(r'^$',login_required(UserInfoView.as_view()),name='user'),# 用户中心--信息页
    # url(r'^order$',login_required(UserOrderView.as_view()),name='order'), # 用户中心--订单页
    # url(r'^address$',login_required(AddressView.as_view()),name='address'), # 用户中心--地址页
    # 但是我们每一个都这样去包住来验证是否已经登陆的话就很复杂，为了解决这个问题，我们引入了Mixin，详情见工具包（utils）

    url(r'^$',UserInfoView.as_view(),name='user'), # 用户中心--信息页
<<<<<<< HEAD
    url(r'^order$',UserOrderView.as_view(),name='order'), # 用户中心--订单页
=======
    url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'), # 用户中心--订单页
>>>>>>> second_dailyfresh
    url(r'^address$',AddressView.as_view(),name='address'),  # 用户中心--地址页



]
