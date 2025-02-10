from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Prefetch, Q, Count
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from tasks.models import Task
from users.forms import RegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, EditProfileForm, CustomPasswordResetConfirmForm, CustomPasswordResetForm

User = get_user_model()


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save()  # Save the form
        return redirect('profile')


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image

        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context


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
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('login')
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        """Log out the user after password change and redirect to login with a message."""
        form.save()
        logout(self.request)  # Log out the user
        messages.success(
            self.request, "Password changed successfully. Please log in again.")
        return redirect(reverse_lazy('login'))  # Redirect to login page


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account Activate. Please Login Now")
            return redirect('login')
        else:
            return HttpResponse('Invalid token or user ID')
    except User.DoesNotExist:
        return HttpResponse('User not found')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    """Using this view, an admin can assign any user to a specific role."""
    user = User.objects.get(id=user_id)
    print(user)

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            print(role)
            user.groups.clear()  # Remove old roles
            user.groups.add(role)  # Add the new role
            messages.success(request, f"User {user.username} has been assigned to the {
                             role.name} role.")
            return redirect('dashboard')
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


@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{
                             group.name}' has been created successfully")
            return redirect("group-list")
    else:
        form = CreateGroupForm()

    return render(request, "admin/create_group.html", {"form": form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related(
        'permissions').annotate(user_count=Count('user')).all()
    return render(request, 'admin/group_list.html', {'groups': groups})


def user_list(request):
    users = User.objects.prefetch_related(
        Prefetch(
            'groups',
            queryset=Group.objects.all(),  # Fetch full Group objects
            to_attr='all_groups'  # Store prefetched groups in an attribute
        )
    )

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'

    return render(request, 'admin/userlist.html', {'users': users})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password_form.html'
    success_url = reverse_lazy('login')
    html_email_template_name = 'registration/reset_password_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)
