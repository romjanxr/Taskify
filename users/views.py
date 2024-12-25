from django.shortcuts import render, redirect
from users.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def register_user(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
