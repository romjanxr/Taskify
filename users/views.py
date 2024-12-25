from django.shortcuts import render, redirect
from users.forms import RegistrationForm
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Doc", username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
