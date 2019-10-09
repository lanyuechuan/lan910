from django.conf.urls import url
from goods import views

urlpatterns = [
    url(r'^$',views.index,name='index') # 天天生鲜首页，那必然在商品模块
]
