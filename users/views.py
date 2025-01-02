from django.shortcuts import render, redirect
from users.forms import RegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required


def register_user(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            return redirect('login')
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print('form is not valid')
            print(form.errors)
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('manager-dashboard')
        else:
            return HttpResponse('Invalid token or user ID')
    except User.DoesNotExist:
        return HttpResponse('User not found')


def is_admin(user: User):
    # Ensures only staff users (admins) can access the view
    return user.groups.filter(name='Admin').exists()


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    """Using this view, an admin can assign any user to a specific role."""
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()  # Remove old roles
            user.groups.add(role)  # Add the new role
            messages.success(request, f"User {user.username} has been assigned to the {
                             role.name} role.")
            return redirect('admin-dashboard')
    else:
        form = AssignRoleForm()

    return render(request, 'admin/assign_role.html', {'user': user, 'form': form})


@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related('groups').all()
    return render(request, 'admin/dashboard.html', {'users': users})


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()

    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{
                             group.name} has been created successfully'")
            return redirect('group-list')

    return render(request, 'admin/create_group.html', {"form": form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})
