from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
# update
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import User
# from .forms import  CustomUserChangeForm
# from django.contrib.auth.forms import  PasswordChangeForm



# Create your views here.
@require_http_methods(['GET','POST'])
def login(request):
    if request.user.is_authenticated:
        redirect('books:index')
    
    if request.method=='POST':
        form=AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('books:index')
    else:
        form=AuthenticationForm()
    context={
        'form':form
    }
    return render(request, 'accounts/login.html',context)

# @require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('books:index')

@require_http_methods(['GET','POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method=='POST':
        form=CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            category_values= form.cleaned_data.get('category', [])
            category_string=','.join(category_values)
            user.category=category_string
            user.save()
            auth_login(request, user)
            return redirect('books:index')
    else:
        form=CustomUserCreationForm()
    context={
        'form':form
    }
    return render(request,'accounts/signup.html',context)

@login_required
@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('books:index')

@login_required
@require_http_methods(['GET','POST'])
def update(request):
    if request.method=='POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            category_values = form.cleaned_data.get('category',[])
            category_string = ','.join(category_values)
            user.category = category_string
            user.save()
            return redirect('books:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context={
        'form':form
    }
    return render(request,'accounts/update.html', context)

@login_required
@require_http_methods(['GET','POST'])
def change_password(request, user_pk):
    if request.method=='POST':
        form=PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('books:index')
    else:
        form=PasswordChangeForm(request.user)
    context={
        'form':form
    }
    return render(request, 'accounts/change_password.html', context)

@login_required
@require_http_methods(['GET'])
def profile(request):
    profiles = User.objects.get(pk = request.user.pk)
    context = {
        'profiles':profiles
    }
    return render(request, 'accounts/profile.html', context)