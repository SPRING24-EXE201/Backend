from django.db import models
from django.utils import timezone


# Create your models here.
# Location
class AdministrativeRegion(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    code_name_en = models.CharField(max_length=100)


class AdministrativeUnit(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    short_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    code_name_en = models.CharField(max_length=100)


class Province(models.Model):
    administrativeRegionId = models.ForeignKey(AdministrativeRegion, on_delete=models.CASCADE)
    administrativeUnitId = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)


class District(models.Model):
    provinceId = models.ForeignKey(Province, on_delete=models.CASCADE)
    administrativeUnitId = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)


class Ward(models.Model):
    districtId = models.ForeignKey(District, on_delete=models.CASCADE)
    administrativeUnitId = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)


class Location(models.Model):
    wardId = models.ForeignKey(Ward, on_delete=models.CASCADE)
    location_detail = models.CharField(max_length=100)


# Cabinet
class Controller(models.Model):
    locationId = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    kafka_id = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    status = models.CharField(max_length=100)


class CabinetType(models.Model):
    type = models.CharField(max_length=100)
    type_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    image_link = models.CharField(max_length=100)
    cost_per_unit = models.FloatField()


class CostVersion(models.Model):
    version = models.CharField(max_length=100)
    from_hour = models.FloatField()
    to_hour = models.FloatField()
    cost = models.FloatField()
    unit = models.CharField(max_length=100)
    status = models.CharField(max_length=100)


class Campaign(models.Model):
    costVersionId = models.ForeignKey(CostVersion, on_delete=models.CASCADE)
    time_start = models.DateTimeField(null=True, blank=True, default=None)
    time_end = models.DateTimeField(null=True, blank=True,default=None)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Cabinet(models.Model):
    controllerId = models.ForeignKey(Controller, on_delete=models.CASCADE)
    cabinetTypeId = models.ForeignKey(CabinetType, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    rental_date = models.CharField(max_length=100)
    cost = models.CharField(max_length=100)
    width = models.CharField(max_length=100)
    height = models.CharField(max_length=100)
    image_link = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    depth = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    virtual_cabinet_id = models.CharField(max_length=100)


class CampaignCabinet(models.Model):
    campaignId = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    cabinetId = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    campaign_id = models.CharField(max_length=100)
    cabinet_id = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Cell(models.Model):
    cabinetId = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    hash_code = models.CharField(max_length=100)
    is_assigned = models.CharField(max_length=100)
    cell_index = models.CharField(max_length=100)
    depth = models.CharField(max_length=100)
    height = models.CharField(max_length=100)
    width = models.CharField(max_length=100)


class CellLog(models.Model):
    cellId = models.ForeignKey(Cell, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    time = models.DateTimeField(null=True, blank=True, default=timezone.now)


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    image_link = models.CharField(max_length=100)


class Order(models.Model):
    orderId = models.CharField(max_length=100)
    total_amount = models.FloatField()
    payment_method = models.CharField(max_length=100)
    order_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    status = models.CharField(max_length=100)


class OrderDetail(models.Model):
    cellId = models.ForeignKey(Cell, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    campaign_id = models.CharField(max_length=100)
    time_start = models.DateTimeField(null=True, blank=True,default=None)
    time_end = models.DateTimeField(null=True, blank=True,default=None)
    sub_total = models.FloatField()
