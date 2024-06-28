from rest_framework import serializers

from users import models


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'email',
            'password',
        )


class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserContactApplication
        fields = (
            'full_name',
            'phone',
            'users',
        )