from django.contrib import admin
from home.models import User, CostVersion, Campaign, CampaignCabinet, CabinetType, Location, Controller, Cabinet, Ward, District


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(CostVersion)
class CostVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'cost', 'from_hour', 'to_hour')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('time_start', 'time_end', 'cost_version_id', 'status')


@admin.register(CampaignCabinet)
class CampaignCabinetAdmin(admin.ModelAdmin):
    list_display = ('campaign_id', 'cabinet_id', 'description')


@admin.register(CabinetType)
class CabinetTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'status', 'image_link', 'cost_per_unit')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('ward_id', 'location_detail')


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'name', 'kafka_id', 'topic', 'status')


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('controller_id', 'cabinetType_id', 'description', 'start_using_date', 'height', 'width', 'depth', 'status', 'image_link', 'virtual_cabinet_id')


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('district_id', 'administrative_unit_id', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('province_id', 'administrative_unit_id', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name')
