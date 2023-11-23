import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.forms.widgets import ClearableFileInput

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600', 'placeholder': 'Username'}))
    # email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3', 'placeholder': 'Password Repeat'}))

    class Meta:
            model = CustomUser
            fields = ['username', 'password1', 'password2']

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     User = get_user_model()
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Este correo electrónico ya está en uso.")
    #     return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600', 'placeholder': 'Username'}), max_length=50)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3', 'placeholder': 'Password'}))


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    profile_picture = forms.ImageField(label='', widget=ClearableFileInput(attrs={'class': 'input-file', 'onchange': 'previewImage()'}))