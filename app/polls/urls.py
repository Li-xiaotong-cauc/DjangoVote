from django.urls import path

from . import views

#app_name是命名空间
app_name = "polls"

urlpatterns = [
    #投票列表
    path('',views.poll_list,name='poll_list'),
    # 投票详情页，用poll_id定位
    path('poll_id=<int:poll_id>/',views.poll_index,name='poll_index'),
    #创建投票页
    path('create/',views.create_poll,name='create_poll'),
    #创建投票API
    path('create_API/',views.create_poll_API,name='create_poll_API'),
    #用户发起的投票列表
    path('my_polls/',views.show_my_polls,name='my_polls'),
    #用户参与的投票列表
    path('voted_polls/',views.show_voted_polls,name='voted_polls'),
    #投票API
    path('vote_API/<int:poll_id>/<int:choice_id>/',views.vote_API,name='vote_API'),
]
