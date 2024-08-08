from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

class User(AbstractUser,BaseModel):
    '''用户模型类'''
    class Meta:
        db_table='df_user'
        verbose_name='用户'
        verbose_name_plural=verbose_name

class Address(BaseModel):
    '''地址模型类'''
    user=models.ForeignKey("User",on_delete=models.CASCADE,verbose_name='所属账户')
    receiver=models.CharField(max_length=20,verbose_name='收件人')
    addr=models.CharField(max_length=256,verbose_name='收件地址')
    zip_code=models.CharField(max_length=6,null=True,verbose_name='邮政编码')