from . authentication import urls as authentication_urls
from . horeca import urls as horeca_urls
from . wine import urls as wine_urls
from . users import urls as users_urls
from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('auth/', include(authentication_urls, namespace='authentication')),
    path('user/', include(users_urls, namespace='users')),
    path('horeca/', include(horeca_urls, namespace='horeca')),
    path('wine/', include(wine_urls, namespace='wine')),
]
