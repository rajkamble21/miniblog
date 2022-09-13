from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Post
from captcha.fields import CaptchaField

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput())   
    email = forms.EmailField(max_length=200, help_text='Required') 
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    
class LoginForm(AuthenticationForm):
    username = UsernameField()
    captcha = CaptchaField()
    password = forms.CharField(widget=forms.PasswordInput())

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['img','title','desc']

        