from django.urls import path
from tasks.views import manager_dashboard, create_task

urlpatterns = [
    path('manager-dashboard/', manager_dashboard),
    path('create-task/', create_task, name='create-task')
]
