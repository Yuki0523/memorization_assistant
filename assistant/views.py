from datetime import date
import json

from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import base

from .models import Register
from .forms import RegistrationForm


class TopView(generic.TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            template_name = 'top_log_in.html'
        else:
            template_name = 'top.html'

        return [template_name]


class RegistrationView(LoginRequiredMixin, generic.CreateView):
    model = Register
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('assistant:registration')

    def form_valid(self, form):
        register = form.save(commit=False)
        register.user = self.request.user
        register.studied_at = date.today()
        register.save()
        messages.success(self.request, '登録しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '登録に失敗しました。')
        return super().form_invalid(form)


class ReviewView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = json.dumps(
            [review.to_dict() for review in Register.objects.filter(user=self.request.user)],
            ensure_ascii=False
        )
        print(context['review_list'])
        return context


class RecordReviewView(LoginRequiredMixin, base.View):
    template_name = 'review.html'

    def get(self, request, *args, **kwargs):
        print(request.method)
        return JsonResponse({'hoge': 'choge'})
