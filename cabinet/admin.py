from django.contrib import admin

from cabinet.models import CostVersion, Cell, Cabinet, CabinetType, Controller, Campaign, CampaignCabinet


# Register your models here.
@admin.register(CostVersion)
class CostVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'cost', 'from_hour', 'to_hour')

    def get_form(self, request, obj=None, **kwargs):
        form = super(CostVersionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['to_hour'].required = False
        return form

@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = (
        'controller_id', 'cabinet_type_id', 'description', 'start_using_date', 'height', 'width', 'depth', 'status',
        'image_link')


@admin.register(CabinetType)
class CabinetTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'status', 'image_link')


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'name', 'kafka_id', 'topic', 'status')


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('cell_index', 'cabinet_id', 'width', 'height', 'depth')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('cost_version', 'time_start', 'time_end', 'description')


@admin.register(CampaignCabinet)
class CampaignCabinetAdmin(admin.ModelAdmin):
    list_display = ('cabinet', 'campaign', 'description')
