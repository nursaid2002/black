from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=1, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=1, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'name', 'is_normal')

    @staticmethod
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exist')
        return value

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.pop('password_confirm')
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords does not same")
        return data


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)
    print('Successfully!')


class RefreshTokenSerializer(TokenRefreshSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)


    def validate(self, data):
        email = data.get('email')
        print(email)
        password = data.get('password')
        print(password)
        print(self.context['request'])

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            print(user)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data