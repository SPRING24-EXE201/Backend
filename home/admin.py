from django.contrib import admin
from home.models import User, CostVersion, Campaign, CampaignCabinet


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

