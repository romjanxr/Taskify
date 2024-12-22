from django.shortcuts import render

# Create your views here.
def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")