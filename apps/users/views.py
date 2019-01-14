import json
import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, logout

from utils.json_fun import to_json_data
from utils.res_code import Code, error_map
from .forms import RegisterForm, LoginForm
# # from users.forms import RegisterForm
from .models import Users

# 导入日志器
logger = logging.getLogger('django')

class RegisterView(View):
    """
    """
    def get(self, request):
        """
        """
        return render(request, 'users/register.html')

    def post(self, request):
        """
        """
        # 1、
        json_data = request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))
        form = RegisterForm(data=dict_data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mobile = form.cleaned_data.get('mobile')

            user = Users.objects.create_user(username=username, password=password, mobile=mobile)
            login(request, user)
            return to_json_data(errmsg="恭喜您，注册成功！")

        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)

            return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)

class LoginView(View):
    """
    user login view
    route: /users/login
    # 1、创建类
    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        return render(request, 'users/login.html')

    def post(self, request):
        """

        :param request:
        :return:
        """
        # 2、获取前端的参数
        try:
            json_data = request.body
            if not json_data:
                return to_json_data(errno=Code.PARAMERR, errmsg="参数为为空，请重新输入！")
            dict_data = json.loads(json_data.decode('utf8'))
        except Exception as e:
            logger.info('错误信息：\n{}'.format(e))
            return to_json_data(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])

         # 3、校验参数
        form = LoginForm(data=dict_data, request=request)

        # 4、返回前端
        if form.is_valid():
            return to_json_data(errmsg="恭喜您，登录成功！")
        else:
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
                # print(item[0].get('message'))   # for test
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串

            return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)


class LogoutView(View):
    """

    """
    def get(self, request):
        logout(request)
        return redirect(reverse("users:login"))

# def _register(request):
#     """
#     register page
#     :param request:
#     :return:
#     """
#     return render(request, 'users/register.html')

# def _login(request):
#     """
#     login page
#     :param request:
#     :return:
#     """
#     return render(request, 'users/login.html')
