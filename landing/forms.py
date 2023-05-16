from django import forms
from django.forms import TextInput, EmailInput

from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        # Включить
        # fields = [""]
        # Исключить
        exclude = [""]

        # Привязываем стили к форме
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                # Подсказка в окне ввада
                'placeholder': 'Ваше имя'
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш email'
            })
        }