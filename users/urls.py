from django.urls import path
from users.views import activate_user, admin_dashboard, create_group, register_user, LoginView, logout_user, group_list, assign_role, user_list

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration', register_user, name='registration'),
    path('logout/', logout_user, name='logout'),
    path('activate/<int:user_id>/<str:token>/',
         activate_user, name='activate-user'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('admin/user-list/', user_list, name='user-list'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role')
]
