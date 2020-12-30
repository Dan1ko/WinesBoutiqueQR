from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . views import *

app_name = 'horeca'

router = DefaultRouter()
router.register('', HorecaViewSet)

urlpatterns = [
    path('list/<int:pk>/', HorecaListViewSet.as_view(), name='horeca_list_by_id'),
    path('list/', HorecaListViewSet.as_view(), name='horeca_list'),
    path('wine_delete/<int:horeca_id>/<int:pk>/', HorecaWineDeleteView.as_view(), name='horeca_wine_delete'),
    path('update/', HorecaUpdateViewSet.as_view(), name='horeca_wines_update'),
    path('', include(router.urls)),
]
