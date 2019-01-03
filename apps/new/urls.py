from django.urls import path
from . import views

# app的名字
app_name = 'new'

urlpatterns = [
    path('',views.index,name="index"),  # 将这条路由命名为index
]