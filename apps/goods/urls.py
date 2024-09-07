from apps.goods import views
from django.contrib import admin
from django.urls import path,include
app_name='goods'
urlpatterns = [#匹配url从上到下来的
    path('',views.index,name='index'),#首页
]
