from rest_framework import serializers

from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'total_amount', 'payment_method', 'order_date', 'status']