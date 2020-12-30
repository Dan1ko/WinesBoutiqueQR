from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    path('', views.DocsView.as_view(), name='index'),
    path('user/', views.UserDocs.as_view(), name='user'),
    path('horeca/', views.HorecaDocs.as_view(), name='horeca'),
    path('wine/', views.VinoDocs.as_view(), name='vino'),
]
