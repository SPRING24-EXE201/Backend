import uuid

from django.db import models
from django.utils import timezone

from cabinet.models import Cell
from exe201_backend.common.custom_id import payment_order_id
from user.models import User


# Create your models here.
class Order(models.Model):
    id = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4)
    payment_order_id = models.IntegerField(null=False, blank=False, unique=True, default=payment_order_id)
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


class Assignment(models.Model):
    id = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4)
    orderDetail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    status = models.BooleanField()


class Event(models.Model):
    id = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4)
    orderDetail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    dataId = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField()
    eventType = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100)
    data = models.CharField(max_length=10000, null=True, blank=True)
