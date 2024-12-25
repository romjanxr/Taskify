from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, create_task

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('user-dashboard/', user_dashboard, name='user-dashboard'),
    path('create-task/', create_task, name='create-task')
]
