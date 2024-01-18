from django.contrib import admin

from order.models import OrderDetail, Order


# Register your models here.

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('cell_id', 'user_id', 'order_id', 'campaign_id', 'time_start', 'time_end', 'sub_total')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'total_amount', 'payment_method', 'order_date', 'status')