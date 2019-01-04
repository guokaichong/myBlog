import logging

from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse

from utils.captcha.captcha import captcha
# 安装图片验证码所需要的 Pillow 模块

from . import constants
from users.models import Users

# 导入日志器
logger = logging.getLogger('django')


class ImageCode(View):
    """
    自定义 图像验证码 视图
    # /image_codes/<uuid:image_code_id>/
    """
    """
    思路:1.从前端js获取访问后台图像验证码的方法 路径!
         2.再通过 符合条件的 路径,访问 图像验证码方法
         3.从路径中获取  image_code_id 作为 后台方法的参数;
         4.
    """

    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()

        # 确保settings.py文件中有配置redis CACHE
        con_redis = get_redis_connection(alias='verify_codes')
        img_key = "img_{}".format(image_code_id).encode('utf-8')
        # 将图片验证码的key和验证码文本保存到redis中，并设置过期时间
        con_redis.setex(img_key, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        logger.info("Image code: {}".format(text))

        return HttpResponse(content=image, content_type="images/jpg")

