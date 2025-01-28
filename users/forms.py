import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from core.mixins import StyledFormMixin
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission

User = get_user_model()


class RegistrationForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password):
            errors.append(
                'Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean(self):  # non field error
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data


class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        print("login form initialized")
        super().__init__(*args, **kwargs)

    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")

    #     if username is not None and password:
    #         self.user_cache = authenticate(
    #             self.request, username=username, password=password
    #         )
    #         user_temp = None
    #         if self.user_cache is None:
    #             try:
    #                 chk_user = User.objects.get(username=username)
    #                 if chk_user.check_password(password):
    #                     user_temp = chk_user
    #             except:
    #                 user_temp = None

    #         if user_temp is None:
    #             raise self.get_invalid_login_error()
    #         else:
    #             self.confirm_login_allowed(user_temp)

    #     return self.cleaned_data


class AssignRoleForm(StyledFormMixin, forms.Form):
    """ Form to assign role for admin """
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label='Select a Role',
    )


class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass
