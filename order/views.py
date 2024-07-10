from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from order import serializers
from order import models


class OrderListAPIView(ListAPIView):
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    permission_classes = [IsAdminUser]


class OrderRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = serializers.OrderUpdateSerializer
    permission_classes = [IsAdminUser]
    queryset = models.Order.objects.all()
    lookup_field = 'id'

