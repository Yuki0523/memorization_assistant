from datetime import date
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models import Max
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import base
from django.views.decorators.csrf import csrf_exempt

from .models import Register
from .models import ReviewRecord
from .forms import RegistrationForm
from .forms import UpdateRegisterForm
from .forms import UpdateReviewRecordForm


class TopView(generic.TemplateView):
    """トップページのビュークラス"""
    def get_template_names(self):
        if self.request.user.is_authenticated:
            template_name = 'top_log_in.html'
        else:
            template_name = 'top.html'

        return [template_name]


class RegistrationView(LoginRequiredMixin, generic.CreateView):
    """"学習内容を登録する画面のビュークラス"""
    model = Register
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('assistant:registration')

    # TODO:要精査
    def form_valid(self, form):
        register = form.save(commit=False)
        register.user = self.request.user
        # TODO:モデル側で auto_new_add=True としたほうがいいのではないか。要検討
        register.studied_at = date.today()
        register.save()
        messages.success(self.request, '登録しました。')
        return super().form_valid(form)

    # TODO:要精査
    def form_invalid(self, form):
        messages.error(self.request, '登録に失敗しました。')
        return super().form_invalid(form)


class ReviewView(LoginRequiredMixin, generic.TemplateView):
    """"復習する画面のビュークラス"""
    template_name = 'review.html'

    def get_context_data(self, **kwargs):
        """条件に該当する学習内容のみをコンテキストに加えるためのオーバーライド

        条件は次のとおり:
            復習回数0回:学習内容の登録日から本日まで1日以上経過しているかどうか
            復習回数1回:最後の復習日から本日まで2日以上経過しているかどうか
            復習回数2回:最後の復習日から本日まで4日以上経過しているかどうか
            復習回数3回:最後の復習日から本日まで8日以上経過しているかどうか
            ・
            ・
            ・
            復習回数n回:最後の復習日から本日まで 2**n 日以上経過しているかどうか"""
        context = super().get_context_data(**kwargs)
        target_list = Register.objects.filter(
            user=self.request.user,
        ).annotate(
            last_date_of_review=Max('reviewrecord__reviewed_at'),
            number_of_review_record=Count('reviewrecord')
        )
        review_list = list()
        today = date.today()
        for target in target_list:
            if target.last_date_of_review:
                if (today - target.last_date_of_review).days >= 2 ** target.number_of_review_record:
                    review_list.append(target)
            else:
                if (today - target.studied_at).days >= 1:
                    review_list.append(target)
        context['review_list'] = json.dumps(
            [review.to_dict() for review in review_list],
            ensure_ascii=False
        )
        return context


# TODO:いずれこの方法はやめてフロントエンド側の工夫でCSRF検証を突破できるようにする
@method_decorator(csrf_exempt, name='dispatch')
class CreateReviewRecordView(LoginRequiredMixin, base.View):
    """復習の結果を非同期通信で記録するビュークラス"""
    template_name = 'review.html'

    def post(self, request, *args, **kwargs):
        result = json.loads(request.body)
        ReviewRecord.objects.create(
            target=Register.objects.filter(pk=result['pk']).first(),
            result=result['result'],
            # TODO:モデル側で auto_new_add=True としたほうがいいのではないか。要検討
            reviewed_at=date.today()
        )
        return JsonResponse({})


class RegisterListView(LoginRequiredMixin, generic.ListView):
    """学習内容を一覧表示する画面のビュークラス"""
    model = Register
    template_name = 'register_list.html'

    def get_queryset(self):
        registers = Register.objects.filter(user=self.request.user).order_by('studied_at')
        return registers


class RegisterDetailView(LoginRequiredMixin, generic.DetailView):
    """学習内容の詳細を閲覧する画面のビュークラス"""
    model = Register
    template_name = 'register_detail.html'

    def get_queryset(self):
        queryset = Register.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        """学習内容に対応する復習の記録の一覧もコンテキストに加えるためのオーバーライド"""
        context = super().get_context_data(**kwargs)
        context['review_list'] = ReviewRecord.objects.filter(
            target=Register.objects.filter(pk=self.kwargs.get('pk')).first()
        ).order_by('reviewed_at')
        return context


class UpdateRegisterView(LoginRequiredMixin, generic.UpdateView):
    """学習内容を編集する画面のビュークラス"""
    model = Register
    template_name = 'update_register.html'
    form_class = UpdateRegisterForm

    def get_queryset(self):
        queryset = Register.objects.filter(user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('assistant:register_detail', kwargs={'pk': self.kwargs['pk']})


class DeleteRegisterView(LoginRequiredMixin, generic.DeleteView):
    """学習内容を削除する画面のビュークラス"""
    model = Register
    template_name = 'delete_register.html'
    success_url = reverse_lazy('assistant:register_list')

    def get_queryset(self):
        queryset = Register.objects.filter(user=self.request.user)
        return queryset


class UpdateReviewRecordView(LoginRequiredMixin, generic.UpdateView):
    """復習の記録を編集する画面のビュークラス"""
    model = ReviewRecord
    template_name = 'update_review_record.html'
    form_class = UpdateReviewRecordForm

    def get_queryset(self):
        queryset = ReviewRecord.objects.filter(target__user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('assistant:register_detail', kwargs={'pk': self.object.target.pk})


class DeleteReviewRecordView(LoginRequiredMixin, generic.DeleteView):
    """復習の記録を削除する画面のビュークラス"""
    model = ReviewRecord
    template_name = 'delete_review_record.html'

    def get_queryset(self):
        queryset = ReviewRecord.objects.filter(target__user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('assistant:register_detail', kwargs={'pk': self.object.target.pk})
