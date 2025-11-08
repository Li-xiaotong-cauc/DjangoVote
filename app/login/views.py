from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from login.models import userInfo


def register_index(request):
    return render(request, 'register.html')

def register_API(request):

    if request.method == "POST": #如果接收到前端传来的POST请求
        #获取数据
        name = request.POST.get("name", "").strip()
        account = request.POST.get("account", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()



        # 验证必填字段,目前还未完成
        errors = {}

        if not name:
            errors["nameErr"] = "请填写姓名!"

        if not account:
            errors["accountErr"] = "请填写账号!"

        if not email:
            errors["emailErr"] = "请填写邮箱!"

        if not password:
            errors["passwordErr"] = "请填写密码"

        if userInfo.objects.filter(account=account).exists():
            errors["accountErr"] = "账号已存在!"

        if userInfo.objects.filter(email=email).exists():
            errors["emailErr"] = "邮箱已存在!"


        if errors:

            context = errors.copy()

            #此处将前端传来的name, account, email更新到context中，
            # 以便在前端页面中显示用户输入的内容，而不是清空
            context.update({
                "name": name,
                "account": account,
                "email": email,
            })
            return render(request, "register.html", context)


        try:
            userInfo.objects.create(
                name=name,
                account=account,
                email=email,
                password=password,
            )

            request.session["account"] = account

            return redirect(reverse('login:login'))

        except IntegrityError:

            errors["accountErr"] = "注册失败，请检查账号或邮箱是否已被使用!"
            context = errors.copy()
            context.update({
                "name": name,
                "account": account,
                "email": email,
            })

            return render(request, "register.html", context)

    return redirect(reverse('login:register'))


def login_index(request):
    return render(request, 'login.html')


def login_API(request):

    if request.method == "GET":

        account = request.GET.get("account", "").strip()
        password = request.GET.get("password", "").strip()

        queryset = userInfo.objects.filter(account=account)

        if not account or not password:
            return render(request, "login.html", {
                "nameErr": "请填写账号和密码",
            })

        if not(queryset.exists()):

                return render(request, "login.html", {
                    "nameErr": "账号不存在!",
                })

        queryset = queryset.filter(password=password)

        if not(queryset.exists()):
                return render(request, "login.html", {
                    "pswErr": "密码错误!",
                })

        #下面这个HTTPResponse是为测试用途，实际项目中应接login_API后续事务
        #return HttpResponse("登录成功!")



        request.session["account"] = queryset[0].account
        # 清除旧的session数据，确保登录状态正确
        request.session.modified = True
        return redirect(reverse('dashboard:index'))

def logout(request):
    # 清除session数据，确保登出状态正确
    request.session.flush()
    return redirect(reverse('login:login'))

