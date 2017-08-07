"""oldboyblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index1),
    url(r'^index1/(?P<type_id>\d+)/', views.index1),
    url(r'^login/', views.login),    # 登录
    url(r'^logout/', views.logout),  # 登出
    url(r'^updown/', views.updown),  # 点赞
    url(r'^comment/', views.comment),  # 异步评论
    url(r'^put_comment/', views.put_comment),  # 异步评论

    url(r'^check_code/', views.check_code),
    # url(r'^register/', views.register),
    url(r'^register1/', views.register1),
    url(r'^upload/', views.upload),
    url(r'^home/(?P<site>\w+)/$', views.home),
    url(r'^home/(?P<site>\w+)/article/(?P<nid>\d+).html$', views.detail),
    url(r'^home/(?P<site>\w+)/(?P<condition>((tag)|(category)|(date)))/(?P<nid>\w+-?\w*).html$', views.filter),





    url(r'^myadmin/', include("myadmin.urls")),  # 后台管理



    url(r'^permit/', include("app02.urls")),

]




















