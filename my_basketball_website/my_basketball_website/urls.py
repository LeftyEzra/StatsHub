from django.contrib import admin
from django.urls import path, include

# To use the media declared in the settings.py file
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('B_Ball.urls')),
    path('statshub_admin/', include('django.contrib.auth.urls')),
    path('statshub_admin/', include('statshub_admin.urls')),
    path('api/', include('API.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Include the media files and Urls here.

# Configure admin titles
admin.site.site_header = "StatsHub Administrative Section"
admin.site.site_title = "StatsHub"
admin.site.index_title = "Welcome To StatsHub Admin Area..."