from django.urls import path
from tasks.views import manager_dashboard

urlpatterns = [
    path('manager-dashboard/', manager_dashboard)
]
