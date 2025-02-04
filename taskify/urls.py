from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, no_permission


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls')),
    path('no-permission/', no_permission, name='no-permission')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
