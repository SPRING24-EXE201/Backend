from django.contrib import admin

from cabinet.models import CostVersion, Cell, Cabinet, CabinetType, Controller

# Register your models here.
@admin.register(CostVersion)
class CostVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'cost', 'from_hour', 'to_hour')


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = (
        'Controller_id', 'CabinetType_id', 'description', 'start_using_date', 'height', 'width', 'depth', 'status',
        'image_link', 'virtual_cabinet_id')


@admin.register(CabinetType)
class CabinetTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'status', 'image_link', 'cost_per_unit')


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = ('Location_id', 'name', 'kafka_id', 'topic', 'status')


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('cell_index', 'Cabinet_id', 'width', 'height', 'depth')
