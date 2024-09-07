from apps.user import views
from django.contrib import admin
from django.urls import path,include
app_name='user'
urlpatterns = [#匹配url从上到下来的
    path("register/",views.register,name='register'),#注册
    path("register_handle/",views.register_handle,name='register_handle'),#注册处理
]
