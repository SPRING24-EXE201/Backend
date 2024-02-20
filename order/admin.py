from django.contrib import admin
from order.models import OrderDetail, Order, Assignment, Event


# Register your models here.
@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('cell_id', 'user', 'order_id', 'time_start', 'time_end', 'sub_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'payment_method', 'order_date', 'status')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderDetail_id', 'email', 'status')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderDetail', 'dataId', 'timestamp', 'eventType', 'email', 'data')

