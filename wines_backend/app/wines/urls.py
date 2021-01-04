from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from backend.docs import urls as docs_urls
from backend.api import urls as api_urls

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET URLS
    path('admin/', admin.site.urls),
    path('api/', include(api_urls, namespace='api')),
    path('api-docs/', include(docs_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
