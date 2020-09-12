from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Register


class LoggedInTestCase(TestCase):
    """全てのテストに共通して必要な事前のログインを追加した TestCase"""

    def setUp(self):
        # ハッシュ値に変換される前の生のパスワードを変数に保持しておく
        self.password = 'TestPassword1234'
        # テスト用ユーザーを作成する
        self.test_user = get_user_model().objects.create_user(
            username='TestUsername1234',
            password=self.password
        )
        # テスト用ユーザーでログインする
        self.client.login(
            username=self.test_user.username,
            password=self.password
        )


class TestRegistrationView(LoggedInTestCase):
    """学習内容を登録する画面のビュークラスのテスト"""

    def test_registration_success(self):
        """登録が成功することを検証する"""
        params = {'question': 'テスト問題文',
                  'answer': 'テスト解答文'}
        self.client.post(reverse_lazy('assistant:registration'), params)
        self.assertEqual(Register.objects.filter(question=params['question']).count(), 1)

    def test_registration_failure(self):
        """登録が失敗することを検証する"""
        params = {'question': '',
                  'answer': ''}
        self.client.post(reverse_lazy('assistant:registration'), params)
        self.assertEqual(Register.objects.filter(question=params['question']).count(), 0)
