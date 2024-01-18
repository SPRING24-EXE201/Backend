
from django.db import models
from django.utils import timezone

from location.models import Location


# Create your models here.
class Controller(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
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
    cost_per_unit = models.FloatField()

    def __str__(self):
        return self.type


class CostVersion(models.Model):
    version = models.CharField(max_length=100)
    from_hour = models.FloatField()
    to_hour = models.FloatField()
    cost = models.FloatField()
    unit = models.CharField(max_length=100)
    status = models.BooleanField()

    def __str__(self):
        return f"{self.version} - {self.cost}"


class Campaign(models.Model):
    cost_version_id = models.ForeignKey(CostVersion, on_delete=models.CASCADE)
    time_start = models.DateTimeField(null=True, blank=True, default=None)
    time_end = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cost_version_id} - {self.status}"


class Cabinet(models.Model):
    controller_id = models.ForeignKey(Controller, on_delete=models.CASCADE)
    cabinetType_id = models.ForeignKey(CabinetType, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    start_using_date = models.CharField(max_length=100)
    height = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField()
    status = models.BooleanField()
    image_link = models.CharField(max_length=100)
    virtual_cabinet_id = models.CharField(max_length=100)


class CampaignCabinet(models.Model):
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    cabinet_id = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.campaign_id} - {self.cabinet_id}"


class Cell(models.Model):
    cabinet_id = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    status = models.PositiveSmallIntegerField()
    hash_code = models.CharField(max_length=100)
    cell_index = models.PositiveSmallIntegerField()
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()

    def __str__(self):
        return f'{self.cell_index} - Cabinet {self.cabinet_id.description}'


class CellLog(models.Model):
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    status = models.BooleanField()
    time = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return f'{self.user_id} - {self.cell_id} - {self.status} at {self.time}'
