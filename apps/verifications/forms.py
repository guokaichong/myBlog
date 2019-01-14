# 在verifications目录下的forms.py文件中定义如下form表单：

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2018/12/3 4:18 PM
  @Auth : Youkou
  @Site : www.youkou.site
  @File : forms.py
  @IDE  : PyCharm
  @Edit : 2018/12/3
-------------------------------------------------
"""
from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from users.models import Users

# 创建手机号的正则校验器
mobile_validator = RegexValidator(r"^1[3-9]\d{9}$", "手机号码格式不正确")


class CheckImgCodeForm(forms.Form):
    """
    check image code
    """
    mobile = forms.CharField(max_length=11, min_length=11, validators=[mobile_validator, ],
                             error_messages={"min_length": "手机号长度有误", "max_length": "手机号长度有误",
                                             "required": "手机号不能为空"})
    image_code_id = forms.UUIDField(error_messages={"required": "图片UUID不能为空"})
    text = forms.CharField(max_length=4, min_length=4,
                           error_messages={"min_length": "图片验证码长度有误", "max_length": "图片验证码长度有误",
                                           "required": "图片验证码不能为空"})

    def clean_mobile(self):
        tel = self.cleaned_data.get('mobile')
        if Users.objects.filter(mobile=tel).count():
            raise forms.ValidationError("手机号已注册，请重新输入！")

        return tel

    def clean(self):
        cleaned_data = super().clean()
        mobile_num = cleaned_data.get('mobile')
        image_uuid = cleaned_data.get('image_code_id')
        image_text = cleaned_data.get('text')

        # 1、获取图片验证码
        try:
            con_redis = get_redis_connection(alias='verify_codes')
        except Exception as e:
            raise forms.ValidationError("未知错误")
        img_key = "img_{}".format(image_uuid).encode('utf8')

        real_image_code_origin = con_redis.get(img_key)   # False

        con_redis.delete(img_key)
        # if not real_image_code_origin:
        #     real_image_code = None
        # else:
        #     real_image_code = real_image_code_origin.decode('utf8')

        real_image_code = real_image_code_origin.decode('utf8') if real_image_code_origin else None

            # 2、判断用户输入的图片验证码是否正确
        if (not real_image_code) or (image_text.upper() != real_image_code):
            raise forms.ValidationError("图片验证码验证失败")

        # 3、判断在60秒内是否有发送短信的记录
        sms_flag_fmt = "sms_flag_{}".format(mobile_num).encode('utf8')
        sms_flag = con_redis.get(sms_flag_fmt)

        if sms_flag:
            raise forms.ValidationError("获取短信验证码过于频繁")







