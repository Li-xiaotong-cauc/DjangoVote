from django.urls import path

from . import views

#命名空间
app_name = "dashboard"

urlpatterns = [
    path('', views.index, name="index"),
    path('welcome/', views.welcome, name="welcome"),
    path('userCenter/', views.userCenter, name="userCenter"),
]
