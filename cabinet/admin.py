from django.contrib import admin

from cabinet.models import CostVersion, Campaign, CampaignCabinet


# Register your models here.
@admin.register(CostVersion)
class CostVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'cost', 'from_hour', 'to_hour')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('cost_version_id', 'time_start', 'time_end', 'status', 'description')

@admin.register(CampaignCabinet)
class CampaignCabinetAdmin(admin.ModelAdmin):
    list_display = ('campaign_id', 'cabinet_id', 'description')