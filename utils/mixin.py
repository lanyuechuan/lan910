# 定义一个类重写as_view方法，那三个用户页面就不需要每一个去包了，因为我们这里把login_required包上as_view封装为了一个函数返回,后面只需要这三个页面的视图函数去继承于我们定义的这个类就可以了
# 继承之后类视图（继承了View）中的as_view方法就直接变为了login_required(as_view())
from django.contrib.auth.decorators import login_required
# 用来判断用户是否成功登录，成功登录才会返回用户中心的三个页面,没有登陆才会跳转到我们setting文件中的指定url(user/login),没有登陆肯定亚奥登陆撒
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls,**initkwargs):
        # 调用父类的as_view，python中调用父类方法用super，第一个参数是自己的类名，后面是参数
        view = super(LoginRequiredMixin,cls).as_view(**initkwargs)
        return login_required(view)