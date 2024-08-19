from django.contrib import admin
from django.urls import path, include

# To use the media declared in the settings.py file
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('B_Ball.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Include the media files and Urls here.

