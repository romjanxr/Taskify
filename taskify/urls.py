from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, no_permission
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls')),
    path('no-permission/', no_permission, name='no-permission')
] + debug_toolbar_urls()
