from django.db import models
from accounts.models import CustomUser


class Register(models.Model):
    """学習内容のモデル"""
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    question = models.CharField(verbose_name='問題', max_length=140)
    answer = models.CharField(verbose_name='解答', max_length=140)
    studied_at = models.DateField(verbose_name='学習日')

    class Meta:
        verbose_name_plural = 'Register'

    def __str__(self):
        return self.question

    def to_dict(self):
        """復習モードでJSONをクライアントサイドに渡す際に必要なインスタンス属性を辞書型で返すメソッド"""
        return {
            'pk': self.pk,
            'question': self.question,
            'answer': self.answer,
        }


class ReviewRecord(models.Model):
    """復習の記録のモデル"""
    target = models.ForeignKey(Register, verbose_name='復習対象', on_delete=models.CASCADE)
    result = models.BooleanField(verbose_name='正答')
    reviewed_at = models.DateField(verbose_name='復習日')

    class Meta:
        verbose_name_plural = 'Review_Record'
