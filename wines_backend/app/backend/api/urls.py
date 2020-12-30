from . authentication import urls as authentication_urls
from . horeca import urls as horeca_urls
from . vino import urls as vino_urls
from . users import urls as users_urls
from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('auth/', include(authentication_urls, namespace='authentication')),
    path('user/', include(users_urls, namespace='users')),
    path('horeca/', include(horeca_urls, namespace='horeca')),
    path('vino/', include(vino_urls, namespace='vino')),
]
