from django import forms
from django.contrib.auth.models import User
from core.models import Customer


class BasicUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name",)


class BasicCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('avatar',)
