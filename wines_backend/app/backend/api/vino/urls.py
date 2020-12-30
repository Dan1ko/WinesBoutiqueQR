from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . views import *

app_name = 'vino'

router = DefaultRouter()
router.register('', WineViewSet)

urlpatterns = [
    path('list/<int:pk>/', WineListViewSet.as_view(), name='wine_list_by_id'),
    path('list/', WineListViewSet.as_view(), name='wine_list'),
    path('', include(router.urls)),
]
