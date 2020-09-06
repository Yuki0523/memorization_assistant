from django import forms

from .models import Register
from .models import ReviewRecord


class RegistrationForm(forms.ModelForm):
    """学習内容を登録するためのフォーム"""
    class Meta:
        model = Register
        fields = ('question', 'answer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RegisterUpdateForm(forms.ModelForm):
    """学習内容を編集するためのフォーム"""
    class Meta:
        model = Register
        fields = ('question', 'answer', 'studied_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ReviewRecordUpdateForm(forms.ModelForm):
    """復習の記録を編集するためのフォーム"""
    class Meta:
        model = ReviewRecord
        fields = ('result', 'reviewed_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
