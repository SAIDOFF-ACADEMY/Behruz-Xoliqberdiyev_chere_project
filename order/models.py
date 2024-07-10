from django.db import models
from products.models import Product
from users.models import User
from django.utils.translation import gettext_lazy as _
from shared.models import BaseModel


class Order(BaseModel):

    class Status(models.TextChoices):
        CREATED = 'created'
        IN_PROGRESS = 'in_progres'
        ON_THE_WAY = 'on_the_way'
        DELIVERED = 'delivered'
        CANCELLED = 'cancelled'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    free_count = models.IntegerField(default=0)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    location = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    status = models.TextField(max_length=100, choices=Status.choices)
    status_changed_at = models.DateTimeField(auto_now=True)
    product_price = models.BigIntegerField()
    total_price = models.BigIntegerField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Order by {self.customer}'

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        db_table = 'orders'

