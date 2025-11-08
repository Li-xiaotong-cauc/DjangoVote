from django.db import models

from login.models import userInfo

# Create your models here.

#投票模型,表示用户发起的投票
class poll(models.Model):
    poll_id = models.AutoField(
        verbose_name='投票ID',
        primary_key=True,
    )
    question = models.CharField(
        verbose_name='问题',
        max_length=50,
        blank = False,
    )
    question_description = models.CharField(
        verbose_name='问题描述',
        max_length=200,
        blank = True,
    )
    pub_date = models.DateTimeField(
        verbose_name='发布时间',
        auto_now_add=True,
    )
    created_by = models.ForeignKey(
        # 外键,关联到userInfo模型,表示该投票是由哪个用户创建的
        userInfo,
        verbose_name='创建人',
        # 级联删除,当用户被删除时,该用户创建的所有投票也会被删除
        on_delete=models.CASCADE,
        related_name='created_polls',
    )

    def __str__(self):
        return f"投票#{self.poll_id}: {self.question}"

    class Meta:
        db_table = 'tb_polls'
        verbose_name = '投票'
        verbose_name_plural = '投票'


#问题模型，关联到投票模型,表示投票的选项
class choice(models.Model):

    poll = models.ForeignKey(
        poll,
        verbose_name='投票',
        on_delete=models.CASCADE,
        related_name='choices',
    )
    choice_text = models.CharField(
        verbose_name='选项文本',
        max_length=50,
        blank = False,
    )
    votes = models.IntegerField(
        verbose_name='票数',
        default=0,
    )

    def __str__(self):
        return self.choice_text

    class Meta:
        db_table = 'tb_choices'
        verbose_name = '选项'
        verbose_name_plural = '选项'


class vote(models.Model):
    #此外键设计可用于统计每个投票的总票数
    poll = models.ForeignKey(
        poll,
        verbose_name='投票',
        on_delete=models.CASCADE,
        related_name='vote_records',
    )
    #此外键设计可用于查询每个选项的投票数
    choice = models.ForeignKey(
        choice,
        verbose_name='选项',
        on_delete=models.CASCADE,
        related_name='vote_records',
    )
    #此外键设计可用于查询每个投票者的投票记录
    voter = models.ForeignKey(
        userInfo,
        verbose_name='投票人',
        on_delete=models.CASCADE,
        related_name='vote_records',
    )
    voted_at = models.DateTimeField(
        verbose_name='投票时间',
        auto_now_add=True,
    )
    class Meta:
        db_table = 'tb_votes'
        verbose_name = '投票记录'
        verbose_name_plural = '投票记录'
        unique_together = ('poll', 'voter')  # 确保每个用户对每个投票只能投一次

