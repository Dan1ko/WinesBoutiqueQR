from rest_framework import permissions, generics, status as http_status
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from backend.utils import CustomJsonRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from copy import deepcopy

UserModel = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (CustomJsonRenderer,)
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        return user


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomJsonRenderer,)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        super().destroy(self, request, *args, **kwargs)
        return Response(status=http_status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = UserModel
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response('Password successfully changed')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (CustomJsonRenderer,)

    def post(self, request):
        username = request.data['username']
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.filter(username=username).first()
            password = UserModel.objects.make_random_password(length=8,
                                                              allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            user.set_password(password)
            user.save()
            return Response('Your password reset!')
        else:
            msg = f'User with username {username} not found!'
            return Response(msg, status=status.HTTP_304_NOT_MODIFIED)
