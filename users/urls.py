from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('registration', views.register_user, name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/',
         views.activate_user, name='activate-user'),
    path('admin/dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin/create-group/', views.create_group, name='create-group'),
    path('admin/group-list/', views.group_list, name='group-list'),
    path('admin/user-list/', views.user_list, name='user-list'),
    path('admin/<int:user_id>/assign-role/',
         views.assign_role, name='assign-role'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password-change/', views.ChangePassword.as_view(), name='password_change'),
    path('password-reset/', views.CustomPasswordResetView.as_view(),
         name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile')
]
