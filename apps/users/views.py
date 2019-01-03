from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

app_name = 'users'

# 基于函数或者基于类视图
# 接受的参数第一个必须为request,并且需要返回一个response对象

class RegisterView(View):
    """
    注册 类视图
    """
    def get(self,request):
        """处理GET请求,返回注册页面"""
        return render(request,'users/register.html')

    def post(self,request):
        """处理POST请求,实现注册逻辑"""
        return HttpResponse('这里实现注册逻辑')
