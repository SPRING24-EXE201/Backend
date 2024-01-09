from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from order.models import Order
from order.web_api.serializers.order_serializer import OrderSerializer


@api_view(['GET'])
def get_orders(self):
    items = Order.objects.all()
    print(items)
    orders = Order.objects.filter(status=True)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_order_by_id(request, order_id):
    """
    Get an order by its id
    """
    try:
        order = Order.objects.get(order_id=order_id)

        if order.status is not True:
            raise NotFound("Order Is Not Active")

        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        raise NotFound("Order Not Found")


@api_view(['POST'])
def create_order(request):
    order_id = request.data.get('order_id')
    total_amount = request.data.get('total_amount')
    payment_method = request.data.get('payment_method')
    order_date = request.data.get('order_date')
    status = request.data.get('status')

    # Check null values
    if order_id is None or total_amount is None or payment_method is None or order_date is None or status is None:
        return Response({'message': 'Invalid input. Please provide all required fields.'}, status=400)

    # Check if order_id already exists
    if Order.objects.filter(order_id=order_id).exists():
        return Response({'message': 'Order with this order_id already exists.'}, status=400)

    # Create new order
    Order.objects.create(
        order_id=order_id,
        total_amount=total_amount,
        payment_method=payment_method,
        order_date=order_date,
        status=status
    )

    return Response({'message': 'Order created successfully!'})

@api_view(['PUT'])
def update_order_by_order_id(request, order_id):
    total_amount = request.data.get('total_amount')
    payment_method = request.data.get('payment_method')
    order_date = request.data.get('order_date')
    status = request.data.get('status')

    # Check null values
    if total_amount is None:
        return Response({'message': 'Invalid input. Please provide the total_amount.'}, status=400)
    if payment_method is None:
        return Response({'message': 'Invalid input. Please provide the payment_method.'}, status=400)
    if order_date is None:
        return Response({'message': 'Invalid input. Please provide the order_date.'}, status=400)
    if status is None:
        return Response({'message': 'Invalid input. Please provide the status.'}, status=400)

    # Check each value to update
    update_values = {
        'total_amount': total_amount,
        'payment_method': payment_method,
        'order_date': order_date,
        'status': status
    }

    # Update the Order object
    Order.objects.filter(order_id=order_id).update(**update_values)

    return Response({'message': 'Order updated successfully!'})

@api_view(['DELETE'])
def delete_all_order(request):
    Order.objects.all().delete()

    return Response({'message': 'Order deleted successfully!'})

@api_view(['DELETE'])
def delete_order_by_order_id(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        if order.status is None:
            return Response({'error': 'Order status is None, cannot delete'}, status=400)
        elif order.status:
            order.status = False 
            order.save()
            return Response({'message': 'Order deleted successfully!'}, status=200)
        else:
            return Response({'error': 'Order cannot be deleted because its status is already False'}, status=400)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)