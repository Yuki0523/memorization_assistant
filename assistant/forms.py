from django import forms

from .models import Register


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('question', 'answer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
