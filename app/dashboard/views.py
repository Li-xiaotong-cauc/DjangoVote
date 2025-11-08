from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from login.models import userInfo
from polls.models import poll, vote

# Create your views here.


def welcome(request):

        return render(request, "welcome.html")

def index(request):

    account = request.session.get("account")

    if not account:
        return redirect(reverse("dashboard:welcome"))




    else:
        # 获取当前时间,确定问候语
        time = datetime.now().strftime("%H")
        #print(time)
        if int(time) in range(5,10):
            greeting = "早上好！"
        elif int(time) in range(10,15):
            greeting = "中午好！"
        elif int(time) in range(15,18):
            greeting = "下午好！"
        else:
            greeting = "晚上好！"

        # 获取最近的九个投票，根据发布时间排序
        nine_recent_polls = poll.objects.all().order_by("-pub_date")[:9]


        display_info = userInfo.objects.filter(account=account)

        # 用户发布的投票数
        publish_count = poll.objects.filter(created_by=display_info[0]).count()

        ###############################参与了用户投票的总人数###############################
        # 获取用户创建的投票
        user_polls = poll.objects.filter(created_by=display_info[0])

        # 统计参与这些投票的独立用户数量
        participate_count_to_self = vote.objects.filter(
            poll__in=user_polls
        ).values('voter').distinct().count()
        ##############################################################################

        ########################用户参与的投票数量（排除自己创建的投票）######################
        participate_count_to_other = vote.objects.filter(
            voter=display_info[0]
        ).exclude(
            poll__created_by=display_info[0]  # 排除自己创建的投票
        ).values('poll').distinct().count()
        ##############################################################################

        return render(request, "index.html", {
            "username": display_info[0].name,
            "greeting": greeting,
            "publish_count": publish_count,
            "participate_count_to_self": participate_count_to_self,
            "participate_count_to_other": participate_count_to_other,
            "nine_recent_polls": nine_recent_polls,
        })


def userCenter(request):

    account = request.session.get("account")


    if not account:
        return redirect(reverse("dashboard:welcome"))



    else:
        # 获取当前时间,确定问候语
        date = datetime.now().strftime("%Y-%m-%d")
        #确定此页面的用户信息
        display_info = userInfo.objects.filter(account=account)
        #用户注册时间
        register_days = (timezone.now() - display_info[0].register_time).days + 1
        #用户发布的投票数
        publish_count = poll.objects.filter(created_by=display_info[0]).count()
        #最近发起的一次投票
        latest_poll = poll.objects.filter(created_by=display_info[0]).order_by("-pub_date").first()
        #最近参与的一次投票(这里返回的是一个vote对象而非poll对象)
        voted_poll_record = vote.objects.filter(voter=display_info[0]).order_by("-voted_at").first()


       ###############################参与了用户投票的总人数###############################
        # 获取用户创建的投票
        user_polls = poll.objects.filter(created_by=display_info[0])

        # 统计参与这些投票的独立用户数量
        participate_count_to_self = vote.objects.filter(
            poll__in=user_polls
        ).values('voter').distinct().count()
        ##############################################################################


        ########################用户参与的投票数量（排除自己创建的投票）######################
        participate_count_to_other = vote.objects.filter(
            voter=display_info[0]
        ).exclude(
            poll__created_by=display_info[0]  # 排除自己创建的投票
        ).values('poll').distinct().count()
        ##############################################################################



        return render(request, "userCenter.html", {
            "now_date": date,
            "username": display_info[0].name,
            "email": display_info[0].email,
            "register_days": register_days,
            "publish_count": publish_count,
            "participate_count_to_self": participate_count_to_self,
            "participate_count_to_other": participate_count_to_other,
            "latest_poll": latest_poll,
            "voted_poll_record": voted_poll_record,
        })
