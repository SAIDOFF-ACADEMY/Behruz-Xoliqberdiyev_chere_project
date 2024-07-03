from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        ref_name = 'AdminUserSerializer'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'full_name',
            'email',
            'password',
        )


class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserContactApplication
        fields = '__all__'
        ref_name = 'AdminUserContactSerializer'


class UserContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserContactApplication
        fields = (
            'is_contacted',
        )
        ref_name = 'AdminUserContactUpdateSerializer'


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = authenticate(email=email, password=password)
        if user is None:
            raise AuthenticationFailed()
        if not user.is_staff:
            raise AuthenticationFailed('Only admin users can log in')
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return {
            'token': token.key,
            }




