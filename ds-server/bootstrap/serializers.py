from rest_framework_simplejwt.serializers import TokenObtainSerializer, RefreshToken, api_settings, update_last_login
from rest_framework_simplejwt.utils import datetime_from_epoch
from django.contrib.auth.models import User
from rest_framework import serializers


class UserTokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)
        data['expires_in'] = datetime_from_epoch(refresh['exp'])

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'username', 'password', 'email', 'last_login', 'is_superuser',
                  'last_name', 'is_staff', 'is_active', 'date_joined', 'first_name')
