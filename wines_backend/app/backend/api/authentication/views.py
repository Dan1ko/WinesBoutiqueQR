from backend.api.authentication.serializers import LoginUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from knox.views import LoginView as KnoxLoginView
from backend.utils import CustomJsonRenderer
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from django.contrib.auth import login


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    renderer_classes = (CustomJsonRenderer,)
    authentication_classes = [BasicAuthentication]

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        if login:
            pass
        else:
            return Response()
        return super(LoginView, self).post(request, format=None)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomJsonRenderer,)

    def post(self, request):
        request._auth.delete()
        return Response()
