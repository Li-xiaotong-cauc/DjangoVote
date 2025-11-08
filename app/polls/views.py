from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from datetime import datetime

from login.models import userInfo
from polls.models import poll, choice, vote


# Create your views here.
def poll_list(request):
    users_count = userInfo.objects.all().count()
    all_polls = poll.objects.all()
    polls_count = poll.objects.all().count()
    return render(request, 'poll_list.html',{
        "users_count": users_count,
        "polls_count": polls_count,
        "polls": all_polls,
    })


def poll_index(request, poll_id):  # 添加poll_id参数
    try:
        # 根据poll_id获取投票对象
        poll_obj = poll.objects.get(poll_id=poll_id)

        # 获取该投票的所有选项
        options = poll_obj.choices.all()

        #获取当前用户账号，用以检查其是否已投票
        account = request.session.get("account")
        user = userInfo.objects.filter(account=account).first()
        # 检查用户是否为投票创建者
        if user == poll_obj.created_by:
            # 如果用户为投票创建者，设置owner为True
            owner = True
        else:
            owner = False

        if account:
            #检查用户是否已投票
            voted = vote.objects.filter(voter=userInfo.objects.get(account=account), poll=poll_obj).exists()

        else:
            voted = False

        if voted:
            # 如果用户已投票，获取其投票记录
            vote_record = vote.objects.get(voter=userInfo.objects.get(account=account), poll=poll_obj)
            voted_choice = vote_record.choice.choice_text
        else:
            voted_choice = None


        return render(request, 'poll_index.html', {
            "poll_id": poll_obj.poll_id,
            "poll_title": poll_obj.question,
            "poll_text": poll_obj.question_description,
            "created_by": poll_obj.created_by.name if poll_obj.created_by else "匿名用户",
            "options": options,
            "pub_date": poll_obj.pub_date.strftime("%Y-%m-%d"),
            "voted": voted,
            "voted_choice": voted_choice,
            "owner": owner,
        })
    except poll.DoesNotExist:
        # 如果投票不存在，返回404页面或错误信息
        return render(request, 'poll_index.html', {
            "error": f"投票ID {poll_id} 不存在"
        })



def create_poll(request):
    return render(request, 'create_poll.html')

def create_poll_API(request):
    if request.method == "POST":
        # 从POST请求中获取表单数据
        pub_account = request.session.get('account')
        if not pub_account:
            return redirect(reverse('dashboard:index'))
        pub_user = userInfo.objects.filter(account=pub_account).first()

        poll_title = request.POST.get('title')
        print("检测到标题:", poll_title)
        poll_text = request.POST.get('text')
        print("检测到内容:", poll_text)
        options = request.POST.getlist('options[]')
        print("检测到选项:", options)

        locate_poll= poll.objects.create(
            created_by = pub_user,
            question = poll_title,
            question_description = poll_text,
            pub_date = timezone.now(),
        )

        for option in options:
            choice.objects.create(
                poll = locate_poll,
                choice_text = option,
            )



        return render(request, 'poll_index.html', {
            "poll_id": locate_poll.poll_id,
            "poll_title": locate_poll.question,
            "poll_text": locate_poll.question_description,
            "created_by": locate_poll.created_by.name,
            "options": locate_poll.choices.all(),
            "pub_date": locate_poll.pub_date,
        })




    else:
        return render(request, 'create_poll.html')


def show_my_polls(request):

    if request.method == "GET":
        account = request.session.get("account")
        user = userInfo.objects.filter(account = account).first()
        return render(request, 'my_polls.html', {
            "user": user,
            "polls": user.created_polls.all(),
        })



    return None

def show_voted_polls(request):
    if request.method == "GET":
        account = request.session.get("account")
        user = userInfo.objects.filter(account = account).first()
        return render(request, 'voted_polls.html', {
            "user": user,
            "voted_polls_records": user.vote_records.all(),
        })


def vote_API(request, poll_id, choice_id):
    # 接收投票POST请求
    if request.method == "GET":
        # 获取到投票者的账号
        account = request.session.get("account")
        # 根据账号获取到投票者的用户对象
        user = userInfo.objects.filter(account=account).first()
        # 根据投票ID获取到投票对象
        poll_obj = poll.objects.filter(poll_id=poll_id).first()
        # 获取到投票对象的所有选项
        options = poll_obj.choices.all()

        if not poll_obj:
            return render(request, 'vote_result.html', {
                "error": f"投票ID {poll_id} 不存在"
            })
        if not choice_id:
            return render(request, 'vote_result.html', {
                "error": "请选择一个选项"
            })
        choice_obj = choice.objects.filter(id=choice_id).first()
        if not choice_obj:
            return render(request, 'vote_result.html', {
                "error": f"选项ID {choice_id} 不存在"
            })

        # 检查用户是否已经投过票
        existing_vote = vote.objects.filter(poll=poll_obj, voter=user).first()
        if existing_vote:
            return render(request, 'vote_result.html', {
                "error": "您已经投过票了，不能重复投票",
                "poll_id": poll_obj.poll_id,
                "poll_title": poll_obj.question,
                "poll_text": poll_obj.question_description,
                "vote_user": user.name,
                "options": options,
                "vote_date": existing_vote.voted_at.strftime("%Y-%m-%d %H:%M"),
                "choice": existing_vote.choice.choice_text,
                "votes": existing_vote.choice.votes,
                "voted": True,  # 用户已经投过票
                "voted_choice": existing_vote.choice.choice_text,
            })

        # 如果用户没有投过票，则进行投票
        choice_obj.votes += 1
        choice_obj.save()
        vote.objects.create(
            poll=poll_obj,
            voter=user,
            choice=choice_obj,
        )
        return render(request, 'vote_result.html', {
            "poll_id": poll_obj.poll_id,
            "poll_title": poll_obj.question,
            "poll_text": poll_obj.question_description,
            "vote_user": user.name,
            "options": options,
            "vote_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "choice": choice_obj.choice_text,
            "votes": choice_obj.votes,
            "voted": True,  # 投票成功后设置为True
            "voted_choice": choice_obj.choice_text,
        })

    return render(request, 'vote_result.html', {
        "error": "投票失败"
    })


def delete_poll_API(request, poll_id):
    # 获取当前操作者的账号，确认是否有权限删除该投票
    account = request.session.get("account")
    user = userInfo.objects.filter(account=account).first()

    # 先检查投票是否存在
    poll_obj = poll.objects.filter(poll_id=poll_id).first()
    if not poll_obj:
        return HttpResponse("投票不存在")

    if user == poll_obj.created_by:
        # 删除投票记录
        vote.objects.filter(poll=poll_id).delete()
        print("投票记录删除成功")
        # 删除投票选项
        choice.objects.filter(poll=poll_id).delete()
        print("投票选项删除成功")
        # 删除投票
        poll.objects.filter(poll_id=poll_id).delete()
        print("投票删除成功")

        return redirect(reverse('dashboard:index'))

    else:
        return HttpResponse("您没有权限删除该投票")
