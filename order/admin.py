from django.contrib import admin

from order.models import OrderDetail


# Register your models here.

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('cell_id', 'user_id', 'order_id', 'campaign_id', 'time_start', 'time_end', 'sub_total')