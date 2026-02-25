from django import forms
from .models import Account

class RegisterationForm(forms.ModelForm):
  model = Account
  fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']