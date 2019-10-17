from django.conf.urls import url
<<<<<<< HEAD
from goods import views

urlpatterns = [
    url(r'^$',views.index,name='index') # 天天生鲜首页，那必然在商品模块
=======
from goods.views import IndexView, DetailView, ListView

urlpatterns = [
    url(r'^index$', IndexView.as_view(), name='index'), # 首页/index
    # 详情页,接收一个参数(数字)，取名为goods_id传给对应视图.如:/goods/1
    url(r'^goods/(?P<goods_id>\d+)$', DetailView.as_view(), name='detail'),
    url(r'^list/(?P<type_id>\d+)/(?P<page>\d+)$', ListView.as_view(), name='list'), # 列表页
    url(r'^', IndexView.as_view(), name='index'), # 列表页
>>>>>>> second_dailyfresh
]
