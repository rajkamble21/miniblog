from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Post
from captcha.fields import CaptchaField, CaptchaTextInput

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={'placeholder': 'enter your email'})) 
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'enter your password'}))
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'placeholder': 'confirm your password'}))   
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {
            'username':forms.TextInput(attrs={'placeholder': 'enter your username'}),
            'first_name':forms.TextInput(attrs={'placeholder': 'enter your first name'}),
            'last_name':forms.TextInput(attrs={'placeholder': 'enter your last name'}),
        }

    
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'enter your username'}))
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'placeholder': 'enter the captcha'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'enter your password'}))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['img','title','category','desc']
        labels = {'img':'post image', 'title':'post title', 'category':'post category', 'desc':'post content'}
        widgets = {
            'img':forms.FileInput(attrs={'class':'box'}), 
            'title':forms.TextInput(attrs={'class':'box'}), 
            'title':forms.TextInput(attrs={'class':'box'}),
            'title':forms.TextInput(attrs={'class':'box'}),
        }

        