import uuid

from django.db import models
from django.utils import timezone

from location.models import Location


# Create your models here.
class Controller(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    kafka_id = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    status = models.BooleanField()

    def __str__(self):
        return self.name


class CabinetType(models.Model):
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    status = models.BooleanField()
    image_link = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class CostVersion(models.Model):
    version = models.CharField(max_length=100)
    from_hour = models.FloatField()
    to_hour = models.FloatField(null=True)
    cost = models.FloatField()
    unit = models.DurationField()
    status = models.BooleanField()

    def __str__(self):
        return f"{self.version} - {self.cost}"


class Campaign(models.Model):
    cost_version = models.CharField(max_length=100, null=False, blank=False, default='UNUSABLE')
    time_start = models.DateTimeField(null=True, blank=True, default=None)
    time_end = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cost_version} - {self.status}"


class Cabinet(models.Model):
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    cabinet_type = models.ForeignKey(CabinetType, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    start_using_date = models.CharField(max_length=100)
    name = models.CharField(max_length=200, default="cabinet", blank=True)
    height = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField()
    status = models.BooleanField()
    image_link = models.CharField(max_length=100)
    column_number = models.IntegerField(default=1)
    row_number = models.IntegerField(default=1)

    def __str__(self):
        return self.description


class CampaignCabinet(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign')
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.campaign} - {self.cabinet}"


class Cell(models.Model):
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField()
    hash_code = models.UUIDField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    cell_index = models.PositiveSmallIntegerField()
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()

    def __str__(self):
        return f'{self.cell_index} - Cabinet {self.cabinet.description}'


class CellLog(models.Model):
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    user = models.IntegerField()
    status = models.BooleanField()
    time = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return f'{self.user} - {self.cell} - {self.status} at {self.time}'
