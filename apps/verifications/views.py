import logging
import json
import string
import random

from django.http import HttpResponse, JsonResponse
from django.views import View
from django_redis import get_redis_connection

from utils.captcha.captcha import captcha
from . import constants
from users.models import Users
from utils.json_fun import to_json_data
from . import forms
from utils.res_code import Code, error_map
from utils.yuntongxun.sms import CCP

# 导入日志器
logger = logging.getLogger('django')


# 1、创建一个类视图
class ImageCode(View):
    """
    define image verification view
    /image_code/<uuid:image_code_id>/

    """

    # 2、从前端获取参数UUID并校验
    def get(self, request, image_code_id):
        # 3、生成验证码文本和验证码图片
        text, image = captcha.generate_captcha()
        # 4、建立redis，并且将图片验证码保存到redis
        con_redis = get_redis_connection(alias='verify_codes')
        img_key = "img_{}".format(image_code_id)  # img_123e4567-e89b-12d3-a456-426655440000
        con_redis.setex(img_key, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        logger.info("Image code: {}".format(text))

        # 5、把验证码图片返回给前端
        return HttpResponse(content=image, content_type='images/jpg')


class CheckUsernameView(View):
    """
    check whether the user exists
    # 1、创建一个类视图
    """

    # 2、校验参数
    def get(self, request, username):
        # 3、查询数据
        # user = Users.objects.filter(username=username)
        # 4、返回校验的结果
        # if not user:
        #     return HttpResponse('可以注册')
        # else:
        #     return HttpResponse('不能注册')
        count = Users.objects.filter(username=username).count()
        # try:
        #     user = Users.objects.get(username=username)
        # except  DoesNotExist:
        #     return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.NODATA])
        data = {
            'username': username,
            'count': count
        }
        # return JsonResponse(data=data)
        return to_json_data(data=data)


class CheckMobileView(View):
    """
    GET mobiles/(?P<mobile>1[3-9]\d{9})/
    """

    def get(self, request, mobile):
        data = {
            'mobile': mobile,
            'count': Users.objects.filter(mobile=mobile).count()
        }
        return to_json_data(data=data)


# 1、创建一个类
class SmsCodesView(View):
    """
    send mobile sms code
    POST /sms_codes/
    """
    def post(self, request):
        # 1、
        json_data = request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))
        # 2、
        form = forms.CheckImgCodeForm(data=dict_data)
        if form.is_valid():
            # 获取手机号
            mobile = form.cleaned_data.get('mobile')
            # 3、
            # 创建短信验证码内容
            sms_num = ''.join([random.choice(string.digits) for _ in range(constants.SMS_CODE_NUMS)])

            # 将短信验证码保存到数据库
            # 确保settings.py文件中有配置redis CACHE
            # Redis原生指令参考 http://redisdoc.com/index.html
            # Redis python客户端 方法参考 http://redis-py.readthedocs.io/en/latest/#indices-and-tables
            # 4、
            redis_conn = get_redis_connection(alias='verify_codes')
            pl = redis_conn.pipeline()

            # 创建一个在60s以内是否有发送短信记录的标记
            sms_flag_fmt = "sms_flag_{}".format(mobile)
            # 创建保存短信验证码的标记key
            sms_text_fmt = "sms_{}".format(mobile)

            # 此处设置为True会出现bug
            try:
                pl.setex(sms_flag_fmt.encode('utf8'), constants.SEND_SMS_CODE_INTERVAL, 1)
                pl.setex(sms_text_fmt.encode('utf8'), constants.SMS_CODE_REDIS_EXPIRES, sms_num)
                # 让管道通知redis执行命令
                pl.execute()
            except Exception as e:
                logger.debug("redis 执行出现异常：{}".format(e))
                return to_json_data(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])

            logger.info("Sms code: {}".format(sms_num))

            # 发送短语验证码
            try:
                result = CCP().send_template_sms(mobile,
                                                 [sms_num, constants.SMS_CODE_REDIS_EXPIRES],
                                                 constants.SMS_CODE_TEMP_ID)
            except Exception as e:
                logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
                return to_json_data(errno=Code.SMSERROR, errmsg=error_map[Code.SMSERROR])
            else:
                if result == 0:
                    logger.info("发送验证码短信[正常][ mobile: %s sms_code: %s]" % (mobile, sms_num))
                    return to_json_data(errno=Code.OK, errmsg="短信验证码发送成功")
                else:
                    logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
                    return to_json_data(errno=Code.SMSFAIL, errmsg=error_map[Code.SMSFAIL])

        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
                # print(item[0].get('message'))   # for test
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串

            return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)
