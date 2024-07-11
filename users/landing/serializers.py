from rest_framework import serializers

from users import models


class UserContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserContactApplication
        fields = (
            'user',
            'message',
            'is_contacted',
        )
