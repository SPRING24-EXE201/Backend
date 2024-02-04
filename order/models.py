import uuid

from django.db import models
from django.utils import timezone

from cabinet.models import Cell
from user.models import User


# Create your models here.
class Order(models.Model):
    id = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4)
    total_amount = models.FloatField()
    payment_method = models.PositiveSmallIntegerField(default=1)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField()

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    time_start = models.DateTimeField(null=True, blank=True, default=None)
    time_end = models.DateTimeField(null=True, blank=True, default=None)
    sub_total = models.FloatField()
