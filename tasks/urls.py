from django.urls import path
from tasks.views import (
    manager_dashboard,
    employee_dashboard,
    dashboard,
    CreateTask
)

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('employee-dashboard/', employee_dashboard, name='employee-dashboard'),
    path('create-task/', CreateTask.as_view(), name='create-task')
]
