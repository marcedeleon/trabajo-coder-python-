from django.forms import ModelForm
from .models import task
from django import forms
from django.contrib.auth.models import User


class pedidos(ModelForm):
    class Meta:
        model = task
        fields = ['titulo', 'descripcion', 'importante', 'usuario']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
