from django.contrib import admin

from location.models import AdministrativeUnit, AdministrativeRegion, Province, Location, Ward, District


# Register your models here.
@admin.register(AdministrativeUnit)
class AdministrativeUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'full_name_en', 'short_name', 'short_name_en', 'code_name', 'code_name_en')


@admin.register(AdministrativeRegion)
class AdministrativeRegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'code_name', 'code_name_en')


@admin.register(Province, )
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'get_administrative_region')

    @admin.display(ordering='province__administrative_region', description='AdministrativeRegion')
    def get_administrative_region(self, obj):
        return obj.administrative_region_id.name


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_detail', 'get_ward', 'get_province', 'get_administrative_region')

    @admin.display(ordering='ward__district__province__administrative_region', description='AdministrativeRegion')
    def get_administrative_region(self, obj):
        return obj.ward_id.district_id.province_id.administrative_region_id.name

    @admin.display(ordering='ward__district__province', description='Province')
    def get_province(self, obj):
        return obj.ward_id.district_id.province_id.name

    @admin.display(ordering='ward__district', description='District')
    def get_district(self, obj):
        return obj.ward_id.district_id.name

    @admin.display(ordering='ward', description='Ward')
    def get_ward(self, obj):
        return obj.ward_id.name

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'get_district', 'get_province', 'get_administrative_region')

    @admin.display(ordering='district__province__administrative_region', description='AdministrativeRegion')
    def get_administrative_region(self, obj):
        return obj.district_id.province_id.administrative_region_id.name

    @admin.display(ordering='district__province', description='Province')
    def get_province(self, obj):
        return obj.district_id.province_id.name

    @admin.display(ordering='district', description='District')
    def get_district(self, obj):
        return obj.district_id.name

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'get_province', 'get_administrative_region')

    @admin.display(ordering='province__administrative_region', description='AdministrativeRegion')
    def get_administrative_region(self, obj):
        return obj.province_id.administrative_region_id.name

    @admin.display(ordering='province', description='Province')
    def get_province(self, obj):
        return obj.province_id.name