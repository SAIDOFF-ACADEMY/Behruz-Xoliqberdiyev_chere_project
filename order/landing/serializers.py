from rest_framework import serializers

from order import models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = (
            'product',
            'count',
            'longitude',
            'latitude',
            'free_count',
            'product_price',
            'total_price',
        )
        ref_name = 'LandingOrderSerializer'
