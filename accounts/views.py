import re
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from core.views import EmailThread
from project.settings import EMAIL_HOST_USER
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            errors = form.errors
            messages.warning(request, errors)
    else:
        form = SignUpForm()   
    return render(request, 'account/signup.html', {'form': form})


def signin(request):
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                if request.user.is_previously_logged_in:
                    messages.success(request, f'Hi {user.email}! You have been logged in')
                    print('logged in')
                else:
                    messages.success(request, f'Hi {user.email}! You have been logged in, however change your password to use the system')
                    print('first timer')
                return redirect('dashboard')
            else:
                message = 'Incorrect email or password'
                messages.warning(request, message)
                print(message)
    else:
        form = forms.LoginForm()
        print('GET loginnn')
    return render(
        request, 'registration/login.html', context={'form': form, 'message': message})


def pre_signout(request):
    return render(request, 'registration/pre_signout.html')


def signout(request):
    logout(request)
    return redirect('homepage')


def users(request):
    users = User.objects.all()
    if request.user.is_superuser:
        users = users.filter(is_staff=True) 
    else:
        users = users.filter(is_staff=False, is_superuser=False)
    context = {'users':users}
    return render(request, 'account/users.html', context)


def user(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {'user':user}
    return render(request, 'account/user.html', context)


def delete_user(request,pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('users')
    context={'object': user}
    return render(request, 'delete_template.html', context)


def user_activation(request, pk):
    user = get_object_or_404(User, pk=pk)
    activated_msg = f"{request.user} activated {user}"
    email = user.email
    deactivated_msg = f"{request.user}dactivated {user}"
    if user.is_active == True:
        user.is_active = False
        user.save()
        messages.info(request, deactivated_msg)
        url =  user.get_absolute_url()
        # Audit.objects.create(event=deactivated_msg, url=url, created_on=timezone.now(), created_by=request.user)
        EmailThread.send_mail('Account deactivation', deactivated_msg, EMAIL_HOST_USER, [email], fail_silently=False)
        return redirect('user', pk=user.id)
    else: 
        user.is_active = True
        user.save()
        messages.info(request, activated_msg)
        url =  user.get_absolute_url()
        # Audit.objects.create(event=activated_msg, url=url, created_on=timezone.now(), created_by=request.user)
        EmailThread.send_mail('Account deactivation', activated_msg, EMAIL_HOST_USER, [email], fail_silently=False)
        return redirect('user', pk=user.id)



@login_required
def first_login(request):
    password_form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            instance = password_form.save(commit=False)
            instance.is_previously_logged_in = True
            # TODO old and new password shouldnt match
            # print(f"{instance.old_password} {instance.password}")
            instance.save()
            update_session_auth_hash(request, password_form.user)
            msg = f"{instance} updated password"
            print(msg)
            messages.success(request, msg)
            return redirect('dashboard')
        else:
            print('password change failed')
            print(password_form.errors)
    return render(request, 'registration/first_login.html', {
        'password_form': password_form,
    })


@login_required
def password_change(request):
    password_form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            msg = f"{password_form.email} updated password"
            print(msg)
            messages.success(request, msg)
            return redirect('dashboard')
        else:
            print('not changed')
            print(password_form.errors)
    return render(request, 'registration/password_change_form.html', {
        'password_form': password_form,
    })
