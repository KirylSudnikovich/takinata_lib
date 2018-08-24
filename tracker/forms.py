from bootstrap_datepicker_plus import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ToDoForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Task name"})
    )
    desc = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Task description", "rows": 3, 'style':'resize:none;'}), required=False
    )
    start_date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y', attrs={"placeholder": "Task start date"}), required=False
    )
    start_time = forms.TimeField(widget=TimePickerInput(attrs={"placeholder": "Task start time"}), required=False)
    end_date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y', attrs={"placeholder": "Task end date"}), required=False
    )
    end_time = forms.TimeField(widget=TimePickerInput(attrs={"placeholder": "Task end time"}), required=False)
