from backend.api.users.views import ResetPasswordView, ChangePasswordView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

app_name = 'user'

router = DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('', include(router.urls)),
]
