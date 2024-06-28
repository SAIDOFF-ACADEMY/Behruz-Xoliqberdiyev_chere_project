from rest_framework import serializers

from products import models


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class FreeProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FreeProduct
        fields = '__all__'