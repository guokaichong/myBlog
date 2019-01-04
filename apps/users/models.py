from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as _UserManager


class UserManager(_UserManager):
    """
    自定义 用户管理器: 修改--> "不需要email字段"
    """

    def create_superuser(self, username, password, email=None, **extra_fields):
        super(UserManager, self).create_superuser(username=password,
                                                  password=password, email=email, **extra_fields)


class Users(AbstractUser):
    """
    向django用户模型 添加 mobile、email_active 字段;
    """
    objects = UserManager()
    """
    当使用createsuperuser管理命令 创建用户时, 将提示输入的字段名列表;
    """
    REQUIRED_FIELDS = ['mobile']   #[必填字段]required_fields

    # help_text在api接口文档中会用到
    # verbose_name在admin站点中会用到
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号", help_text='手机号',
                              error_messages={'unique': "此手机号已注册"}  # 指定报错的中文信息
                              )
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = "tb_users"   # 指明数据库表名
        verbose_name = "用户"    # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):  # 打印对象时调用
        return self.username