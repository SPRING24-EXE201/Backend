from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from order.models import Order
from order.web_api.serializers.order_serializer import OrderSerializer


@api_view(['GET'])
def get_order(self):
    items = Order.objects.all()
    print(items)
    serializer = OrderSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_order(request):
    # If primary key attribute is set to a value and such primary key already exists, then Model.save() performs UPDATE,
    # but Model.objects.create() raises IntegrityError.
    Order.objects.create(order_id=request.data.get('order_id'),
                         total_amount=request.data.get('total_amount'),
                         payment_method=request.data.get('payment_method'),
                         order_date=request.data.get('order_date'),
                         status=request.data.get('status'))

    return Response({'message': 'Order created successfully!'})

@api_view(['PUT'])
def update_order(request):
    Order.objects.filter(order_id=request.data.get('order_id')).update(
        total_amount=request.data.get('total_amount'),
        payment_method=request.data.get('payment_method'),
        order_date=request.data.get('order_date'),
        status=request.data.get('status'))

    return Response({'message': 'Order updated successfully!'})

# @api_view(['DELETE'])
# def delete_order(request):
#     # Order.objects.filter(order_id=request.data.get('order_id')).delete(
        
#     # )
#     Order.objects.all().delete()

#     return Response({'message': 'Order deleted successfully!'})

@api_view(['DELETE'])
def delete_order(request):
    order_id = request.data.get('order_id')
    if order_id is not None:
        try:
            order = Order.objects.get(order_id=order_id)
            order.delete()
            return Response({'message': 'Order deleted successfully!'})
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=404)
    else:
        return Response({'message': 'No order_id provided'}, status=400)