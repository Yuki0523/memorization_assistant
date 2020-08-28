from datetime import date
import json

from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import base
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Register
from .models import ReviewRecord
from .forms import RegistrationForm
from .forms import RegisterUpdateForm
from .forms import ReviewRecordUpdateForm


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
        return context


@method_decorator(csrf_exempt, name='dispatch')
class RecordReviewView(LoginRequiredMixin, base.View):
    template_name = 'review.html'

    def post(self, request, *args, **kwargs):
        result = json.loads(request.body)
        ReviewRecord.objects.create(
            target=Register.objects.filter(pk=result['pk']).first(),
            result=result['result'],
            reviewed_at=date.today()
        )
        return JsonResponse({})


class RegisterListView(LoginRequiredMixin, generic.ListView):
    model = Register
    template_name = 'register_list.html'

    def get_queryset(self):
        registers = Register.objects.filter(user=self.request.user).order_by('studied_at')
        return registers


class RegisterDetailView(LoginRequiredMixin, generic.DetailView):
    model = Register
    template_name = 'register_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = ReviewRecord.objects.filter(
            target=Register.objects.filter(pk=self.kwargs.get('pk')).first()
        ).order_by('reviewed_at')
        print(self.kwargs.get('pk'))
        print(Register.objects.filter(pk=self.kwargs.get('pk')).first())
        print(context['review_list'])
        return context


class RegisterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Register
    template_name = 'register_update.html'
    form_class = RegisterUpdateForm

    def get_success_url(self):
        return reverse_lazy('assistant:register_detail', kwargs={'pk': self.kwargs['pk']})


class RegisterDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Register
    template_name = 'register_delete.html'
    success_url = reverse_lazy('assistant:register_list')


class ReviewRecordUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ReviewRecord
    template_name = 'review_record_update.html'
    form_class = ReviewRecordUpdateForm

    def get_success_url(self):
        return reverse_lazy('assistant:register_detail',
                            kwargs={'pk': self.object.target.pk})
