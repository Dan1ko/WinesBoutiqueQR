from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('token/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
