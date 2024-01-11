from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import JsonResponse, HttpResponse

from order.models import Order
from order.web_api.serializers.order_serializer import OrderSerializer

@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        orders = Order.objects.filter(status=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
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
    
@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, order_id):
    if request.method == 'GET':
        if order_id:
            order = Order.objects.get(order_id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
    elif request.method == 'PUT':
        if order_id:
            total_amount = request.data.get('total_amount')
            payment_method = request.data.get('payment_method')
            order_date = request.data.get('order_date')
            status = request.data.get('status')

            # Check null values
            if total_amount is None or payment_method is None or order_date is None or status is None:
                return Response({'message': 'Invalid input. Please provide all required fields.'}, status=400)

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
    elif request.method == 'DELETE':
        if order_id:
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
        else:
            Order.objects.all().delete()
            return Response({'message': 'All orders deleted successfully!'})
    else:
        return HttpResponse(status=405)  # Method Not Allowed    