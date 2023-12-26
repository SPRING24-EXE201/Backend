from django.contrib import admin

from cabinet.models import CostVersion


# Register your models here.
@admin.register(CostVersion)
class CostVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'cost', 'from_hour', 'to_hour')