from apps.user.views import RegisterView,ActiveView,LoginView
from django.contrib import admin
from django.urls import path,include
app_name='user'
urlpatterns = [#匹配url从上到下来的
    # path("register/",views.register,name='register'),#注册
    # path("register_handle/",views.register_handle,name='register_handle'),#注册处理
    path('register/',RegisterView.as_view(),name='register'),#注册
    path('active/<str:token>',ActiveView.as_view(),name='active'),#用户激活
    path('login/',LoginView.as_view(),name='login'),#登录
]
