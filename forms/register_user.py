# register_user.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from config.models import Employee

class EmployeeRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        # Ensure the username is linked to an Employee entry and not already a User
        if not Employee.objects.filter(resource_item=username).exists():
            raise forms.ValidationError("No employee found with this username.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username
