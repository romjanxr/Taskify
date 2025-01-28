from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Prefetch
from django.db.models import Q, Count
from tasks.models import Task
from users.forms import RegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm

User = get_user_model()


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


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm


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


def is_admin(user):
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
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(),
                 to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'

    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')),
    )

    # Data for role chart
    groups = Group.objects.annotate(user_count=Count('user'))
    roles = [group.name for group in groups]
    role_counts = [group.user_count for group in groups]
    return render(request, 'admin/analytics.html', {
        'users': users,
        'counts': counts,
        'roles': roles,
        'role_counts': role_counts
    })


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


def user_list(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(),
                 to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'

    return render(request, 'admin/userlist.html', {'users': users})
