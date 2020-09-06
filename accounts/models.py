from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ユーザーのモデル"""

    class Meta:
        verbose_name_plural = 'CustomUser'
