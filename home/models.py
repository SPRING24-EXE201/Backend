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
    administrative_region_id = models.ForeignKey(AdministrativeRegion, on_delete=models.CASCADE)
    administrative_unit_id = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)


class District(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)
    administrative_unit_id = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)


class Ward(models.Model):
    district_id = models.ForeignKey(District, on_delete=models.CASCADE)
    administrative_unit_id = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)


class Location(models.Model):
    ward_id = models.ForeignKey(Ward, on_delete=models.CASCADE)
    location_detail = models.CharField(max_length=100)


# Cabinet
class Controller(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    kafka_id = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    status = models.BooleanField()


class CabinetType(models.Model):
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    status = models.BooleanField()
    image_link = models.CharField(max_length=100)
    cost_per_unit = models.FloatField()


class CostVersion(models.Model):
    version = models.CharField(max_length=100)
    from_hour = models.FloatField()
    to_hour = models.FloatField()
    cost = models.FloatField()
    unit = models.CharField(max_length=100)
    status = models.BooleanField()


class Campaign(models.Model):
    cost_version_id = models.ForeignKey(CostVersion, on_delete=models.CASCADE)
    time_start = models.DateTimeField(null=True, blank=True, default=None)
    time_end = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField()
    description = models.CharField(max_length=100)


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


class Cell(models.Model):
    cabinet_id = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    status = models.PositiveSmallIntegerField()
    hash_code = models.CharField(max_length=100)
    cell_index = models.PositiveSmallIntegerField()
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()


class CellLog(models.Model):
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    status = models.BooleanField()
    time = models.DateTimeField(null=True, blank=True, default=timezone.now)


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField()
    image_link = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=200)


class Order(models.Model):
    order_id = models.CharField(max_length=100)
    total_amount = models.FloatField()
    payment_method = models.PositiveSmallIntegerField()
    order_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    status = models.BooleanField()



class OrderDetail(models.Model):
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    campaign_id = models.IntegerField()
    time_start = models.DateTimeField(null=True, blank=True, default=None)
    time_end = models.DateTimeField(null=True, blank=True, default=None)
    sub_total = models.FloatField()
