from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Post, Category
from django.contrib import messages
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from blog.tokens import account_activation_token 
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage 

# Create your views here.
def home(request):
    posts = None
    count = None
    categories = Category.objects.all()
    count = Post.objects.all().count()
    category_id = request.GET.get('category')
    if category_id:
        posts = Post.objects.filter(category=category_id)
    else:
        posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts, 'categories':categories, 'count':count})

def about(request):
    return render(request, 'blog/about.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        print(gps)
        print(full_name)
        return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'gps':gps})
    else:
        return HttpResponseRedirect('login')
    

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return HttpResponseRedirect('/dashboard/')           
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
    

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():       
            user = form.save(commit=False)  
            user.is_active = False
            user = form.save()
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            messages.success(request, "We have send conformation link to your email id")
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

def activate(request, uidb64, token):  
    # User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        group = Group.objects.get(name="Author")
        user.groups.add(group)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.') 
        return HttpResponseRedirect('/login/') 
    else:  
        return HttpResponse('Activation link is invalid!')  



def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                form = PostForm()
                messages.success(request, "Post added successfully!")
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, request.FILES, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, "Post updated successfully!")
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            messages.success(request, 'Post deleted successfully!')
            return HttpResponseRedirect('/dashboard/')  
    else:
        return HttpResponseRedirect('/login/')