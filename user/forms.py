from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'apx-form-input'}))
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'apx-form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'apx-form-input', 'hx-get': "/user/check_us/", 'hx-trigger': 'keyup delay:300ms', 'hx-target': '#user-check', 'hx-swap': 'innerHTML'}))
    password1 = forms.CharField(max_length=150, required=True, label='Password' ,
                               widget=forms.PasswordInput(attrs={'class': 'apx-form-input'}))
    password2 = forms.CharField(max_length=150, required=True, label='Repeat Password',
                                widget=forms.PasswordInput(attrs={'class': 'apx-form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {'username': 'Username',
                  'email': 'E-mail',
                  'password1': 'Password',
                  'password2': 'Repeat Password',
                  'first_name': 'First Name',
                  'last_name': 'Last Name',
                  }
        widgets = {
            'email':  forms.TextInput(attrs={'class': 'apx-form-input', 'hx-get': "/user/check_em/", 'hx-trigger': 'keyup delay:300ms', 'hx-target': '#email-check', 'hx-swap': 'innerHTML'}),
            'first_name':  forms.TextInput(attrs={'class': 'apx-form-input'}),
            'last_name':  forms.TextInput(attrs={'class': 'apx-form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Email is used!')
