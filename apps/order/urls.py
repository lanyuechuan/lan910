<<<<<<< HEAD
"""new_dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

]
=======
from django.conf.urls import url
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView, CommentView

urlpatterns = [
    url(r'^place$', OrderPlaceView.as_view(), name='place'), # 提交订单页面显示
    url(r'^commit$', OrderCommitView.as_view(), name='commit'), # 提交创建
    url(r'^pay$', OrderPayView.as_view(), name='pay'), # 订单支付
    url(r'^check$', CheckPayView.as_view(), name='check'), # 查询支付订单结果
    url(r'^comment/(?P<order_id>.+)$', CommentView.as_view(), name='comment'), # 订单评论
]
>>>>>>> second_dailyfresh
