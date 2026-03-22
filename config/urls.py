from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # set_language view
]

urlpatterns += i18n_patterns(
    path('', include('adminapp.urls')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
