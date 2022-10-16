# swagger imports
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

admin.site.site_header = "POS"
admin.site.site_title = "POS Admin Portal"
admin.site.index_title = "Welcome to POS Admin Portal"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("pos_users.urls")),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)