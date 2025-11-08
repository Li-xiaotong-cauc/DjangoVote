from django.urls import path

from . import views

#app_name是命名空间
app_name = "login"

urlpatterns = [
    #注册页面
    path("register", views.register_index, name="register"),
    #注册API
    path("register_API/", views.register_API, name="register_API"),
    #登录页面
    path("", views.login_index, name="login"),
    #登录API
    path("login_API/", views.login_API, name="login_API"),
    #登出API
    path("logout/", views.logout, name="logout"),

]