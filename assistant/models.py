from accounts.models import CustomUser
from django.db import models


class Register(models.Model):
    """学習の記録モデル"""
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    question = models.CharField(verbose_name='問題', max_length=140)
    answer = models.CharField(verbose_name='解答', max_length=140)
    studied_at = models.DateField(verbose_name='学習日')

    class Meta:
        verbose_name_plural = 'Register'

    def __str__(self):
        return self.question

    def to_dict(self):
        return {
            'pk': self.pk,
            'question': self.question,
            'answer': self.answer,
        }


class ReviewRecord(models.Model):
    """復習の記録モデル"""
    target = models.ForeignKey(Register, verbose_name='復習対象', on_delete=models.PROTECT)
    result = models.BooleanField(verbose_name='正答')
    reviewed_at = models.DateField(verbose_name='復習日')

    class Meta:
        verbose_name_plural = 'Review_Record'
