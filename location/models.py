from django.db import models
from exe201_backend.common.custom_id import location_custom_id, district_custom_id, province_custom_id, ward_custom_id
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
    administrative_region = models.ForeignKey(AdministrativeRegion, on_delete=models.CASCADE)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    id = models.CharField(max_length=17, unique=True, default=province_custom_id, editable=False, primary_key=True)

    def __str__(self):
        return self.full_name


class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    id = models.CharField(max_length=17, unique=True, default=district_custom_id, editable=False, primary_key=True)

    def __str__(self):
        return self.full_name


class Ward(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    full_name_en = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)
    id = models.CharField(max_length=17, unique=True, default=ward_custom_id, editable=False, primary_key=True)

    def __str__(self):
        return self.full_name


class Location(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null = True, blank = True)
    location_detail = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100, blank= True)
    latitude = models.FloatField(null = True, blank = True)
    longitude = models.FloatField(null = True, blank = True)
    id = models.CharField(max_length=17, unique=True, default=location_custom_id, editable=False, primary_key=True)

    def get_display_name(self):
        if self.location_name:
            return self.location_name
        elif self.location_detail:
            return self.location_detail
        elif self.ward:
            return str(self.ward)
        else:
            return "Unknown"

    def __str__(self):
        if self.location_name:
            return self.location_name
        elif self.location_detail:
            return self.location_detail
        elif self.ward:
            return str(self.ward)
        else:
            return "Unknown"




