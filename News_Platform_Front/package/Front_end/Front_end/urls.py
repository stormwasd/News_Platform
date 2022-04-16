"""Front_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from newsapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Front_Page),  # 显示欢迎页面，点击欢迎页面将转到首页(home/)
    path('home/', views.Home_Page),  # 首页将显示最新资讯，点击首页将刷新
    path('Show_Detail/', views.Show_Detail),  # 每条资讯的详情
    path('News_/', views.News)  # 资讯列表页
]
