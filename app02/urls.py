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
from app02 import views
from django.conf.urls import include

urlpatterns = [
    # permit/user.html
    url(r'^user.html$', views.permit),  # 模拟登录，在数据库查询权限，把权限记录到session
    url(r'^order.html$', views.show),  # 个人登录后显示权限


    url(r'^menu$', views.menu),  # 个人登录后显示权限


]




















