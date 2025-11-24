from django.db import models


class userInfo(models.Model):
    account = models.CharField(
        verbose_name='账号',
        max_length=20,
        unique=True,
    )
    name = models.CharField(
        verbose_name='姓名',
        max_length=10,
        help_text='请输入姓名',
    )
    email = models.EmailField(
        verbose_name='邮箱',
        unique=True,
    )
    password = models.CharField(
        verbose_name='密码',
        max_length=16,
        help_text='请输入密码',
    )
    register_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True,
    )
    avatar_name = models.CharField(
        verbose_name='头像名称',
        max_length=150,
        blank = True,
        null = True,
        help_text = '用户头像的文件名',
    )

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

