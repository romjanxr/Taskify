from django.urls import path
from tasks import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager-dashboard'),
    path('employee-dashboard/', views.employee_dashboard,
         name='employee-dashboard'),
    path('task-list/', views.view_task, name='task-list'),
    path('create-task/', views.CreateTask.as_view(), name='create-task'),
    path('view-task/<int:id>/', views.TaskDetail.as_view(), name='view-task-detail'),
    path('update-task/<int:id>/', views.UpdateTask.as_view(), name='update-task'),
    path('delete-task/<int:id>/', views.delete_task, name='delete-task')
]
