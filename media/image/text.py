from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(
        verbose_name='问题',
        max_length=200,
    )
    pub_date = models.DateTimeField(
        verbose_name='发布时间',
        auto_now_add=True,
    )
    # 新增属性
    description = models.TextField(
        verbose_name='描述',
        max_length=500,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name='是否活跃',
        default=True
    )
    end_date = models.DateTimeField(
        verbose_name='结束时间',
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        User,
        verbose_name='创建者',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = '投票'
        verbose_name_plural = '投票'


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll,
        verbose_name='所属投票',
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.CharField(
        verbose_name='选项文本',
        max_length=200
    )
    votes = models.IntegerField(
        verbose_name='票数',
        default=0
    )

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = '选项'
        verbose_name_plural = '选项'


class Vote(models.Model):
    #此外键设计可用于统计每个投票的总票数
    poll = models.ForeignKey(
        Poll,
        verbose_name='投票',
        on_delete=models.CASCADE,
        related_name='votes',
    )
    #此外键设计可用于查询每个选项的投票数
    choice = models.ForeignKey(
        Choice,
        verbose_name='选项',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    #此外键设计可用于查询每个投票者的投票记录
    voter = models.ForeignKey(
        User,
        verbose_name='投票者',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    voted_at = models.DateTimeField(
        verbose_name='投票时间',
        auto_now_add=True
    )

    class Meta:
        verbose_name = '投票记录'
        verbose_name_plural = '投票记录'
        unique_together = ('poll', 'voter')  # 确保每个用户对每个投票只能投一次
