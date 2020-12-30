from django.contrib.auth import authenticate
from backend.apps.users.models import User
from rest_framework import serializers


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            if User.objects.filter(username__iexact=username).exists():
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)
            else:
                msg = {'message': 'Данный пользователь не зарегистрирован.',
                       'register': False}
                raise serializers.ValidationError(msg)
            if not user:
                msg = {
                    'message': 'Невозможно войти с предоставленными учетными данными.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Должны быть указаны "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
