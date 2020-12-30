from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        read_only_fields = ['id']
        exclude = ("email", "first_name", "last_name", "last_login", "is_superuser", "is_staff", "is_active",
                   "date_joined", "groups", "user_permissions", "updated_at")
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance=instance, validated_data=validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = UserModel
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
