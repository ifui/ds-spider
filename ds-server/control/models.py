from django.db import models


# Create your models here.


class Server(models.Model):
    name = models.CharField(max_length=255)  # 服务器别名
    host = models.CharField(max_length=20)  # 服务器地址
    port = models.PositiveIntegerField()  # 服务器端口
    username = models.CharField(
        max_length=255, null=True, blank=True, default=None)  # 登录用户名
    password = models.CharField(
        max_length=255, null=True, blank=True, default=None)  # 登录密码
    to_email = models.EmailField(null=True, blank=True, default=None)  # 通知邮箱地址
