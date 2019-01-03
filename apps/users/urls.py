from django.urls import path
from . import views

# app的名字
app_name = 'users'

# 配置路由时,使用类视图的as_views()方法来添加
urlpatterns = [

    # 视图函数：注册
    # url(r'^register/$', views.register, name='register'),

    # 类视图：注册
    path('register/',views.RegisterView.as_view(),name="register")

]
