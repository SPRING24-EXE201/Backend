from django.db import models
from utils.custom_id import location_custom_id, district_custom_id, province_custom_id, ward_custom_id

class AdministrativeRegion(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    code_name_en = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AdministrativeUnit(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    short_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    code_name_en = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Province(models.Model):
    administrative_region_id = models.ForeignKey(AdministrativeRegion, on_delete=models.CASCADE)
    administrative_unit_id = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    id = models.CharField(max_length=17, unique=True, default=province_custom_id, editable=False, primary_key=True)

    def __str__(self):
        return self.full_name


class District(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)
    administrative_unit_id = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    id = models.CharField(max_length=17, unique=True, default=district_custom_id, editable=False, primary_key=True)

    def __str__(self):
        return self.full_name


class Ward(models.Model):
    district_id = models.ForeignKey(District, on_delete=models.CASCADE)
    administrative_unit_id = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    id = models.CharField(max_length=17, unique=True, default=ward_custom_id, editable=False, primary_key=True)

    def __str__(self):
        return self.full_name


class Location(models.Model):
    ward_id = models.ForeignKey(Ward, on_delete=models.CASCADE, null = True, blank = True)
    location_detail = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100, blank=True)
    
