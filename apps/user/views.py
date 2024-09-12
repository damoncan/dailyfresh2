from django.shortcuts import render,redirect
from django.urls import reverse
import re
from apps.user.models import User
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail

def register(request):
   '''注册'''
   if request.method == 'GET':
        """显示注册页面"""
        return render(request,'register.html')
   else:
        """进行注册处理"""
        #接收数据
        username=request.POST.get('user_name')
        password=request.POST.get('pwd')
        email=request.POST.get('email')
        allow=request.POST.get('allow')
        #数据校验
        if not all([username,password,email]):
            #数据不完整
            return render(request,'register.html',{'errmsg':'数据不完整'})
        #校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':'邮箱格式不正确'})
        if allow != 'on':
            return render(request,'register.html',{'errmsg':'请同意协议'})
        #校验用户名是否重复
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            user=None
        if user:
            #用户名已存在
            return render(request,'register.html',{'errmsg':'用户名已存在'})
        #进行业务处理
        user = User.objects.create_user(username,email,password)
        user.is_active=0#刚注册用户的时候它不应该是被激活的
        user.save()
        #返回应答，跳转到首页
        return redirect(reverse('goods:index'))

def register_handle(request):
    """进行注册处理"""
    #接收数据
    username=request.POST.get('user_name')
    password=request.POST.get('pwd')
    email=request.POST.get('email')
    allow=request.POST.get('allow')
    #数据校验
    if not all([username,password,email]):
        #数据不完整
        return render(request,'register.html',{'errmsg':'数据不完整'})
    #校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request,'register.html',{'errmsg':'邮箱格式不正确'})
    if allow != 'on':
        return render(request,'register.html',{'errmsg':'请同意协议'})
    #校验用户名是否重复
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        user=None
    if user:
        #用户名已存在
        return render(request,'register.html',{'errmsg':'用户名已存在'})
    #进行业务处理
    user = User.objects.create_user(username,email,password)
    user.is_active=0#刚注册用户的时候它不应该是被激活的
    user.save()
    #返回应答，跳转到首页
    return redirect(reverse('goods:index'))


#不同的请求方法对应的是哪个函数
class RegisterView(View):
    def get(self,request):
        '''显示注册页面'''
        return render(request,'register.html')
    def post(self,request):
        """进行注册处理"""
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')


        # 数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})


        # 进行业务处理
        user = User.objects.create_user(username, email, password)
        user.is_active = 0  # 刚注册用户的时候它不应该是被激活的
        user.save()

        # 发送激活邮件，包括激活链接，http://172.0.0.1:8000/user/active/3
        #激活链接中需要包含用户的身份信息，并且要对身份信息进行加密
        #加密用户的身份信息，生成加密token
        serializer=Serializer(settings.SECRET_KEY,3600)
        info={'confirm':user.id}
        token=serializer.dumps(info)#bytes
        token=token.decode()
        #发邮件
        send_register_active_email.delay(email,username,token)
        # 返回应答，跳转到首页
        return redirect(reverse('goods:index'))

# /user/active/
class ActiveView(View):
    def get(self,request,token):
        '''进行用户激活'''
        #进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info=serializer.loads(token)
            # 打印出解码后的信息，方便调试
            print(f"Decoded token info: {info}")
            #获取待激活用户的id
            user_id=info['confirm']
            print(f"User ID from token: {user_id}")
            #根据id获取用户信息
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()
            #跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse('激活链接已过期')

# /user/login/
class LoginView(View):
    '''登录'''
    def get(self,request):
        return render(request,'login.html')