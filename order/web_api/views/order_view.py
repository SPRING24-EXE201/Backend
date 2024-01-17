from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from order.pagination import CustomPageNumberPagination

from order.models import Order
from order.web_api.serializers.order_serializer import OrderSerializer, OrderByUserSerializer


@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all().order_by('order_detail__time_start')
        orders = Order.objects.filter(status=True).order_by('order_detail__time_start')
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
    try:
        if request.method == 'GET':
            if order_id:
                try:
                    order = Order.objects.get(order_id=order_id)
                except Order.DoesNotExist:
                    return Response({'error': 'Order not found'}, status=404)
                serializer = OrderSerializer(order)
                return Response(serializer.data)
        elif request.method == 'PUT':
            if order_id:
                serializer = OrderSerializer(data=request.data)
                if serializer.is_valid():
                    try:
                        # Check if the order exists
                        order = Order.objects.get(order_id=order_id)
                        # Update the order
                        serializer.update(order, serializer.validated_data)
                        return Response({'message': 'Order updated successfully!', 'order': serializer.data})
                    except Order.DoesNotExist:
                        return Response({'error': 'Order with id {} not found'.format(order_id)}, status=404)
                else:
                    return Response(serializer.errors, status=400)
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
                        return Response({'error': 'Order cannot be deleted because its status is already False'},
                                        status=400)
                except Order.DoesNotExist:
                    return Response({'error': 'Order not found'}, status=404)
            else:
                Order.objects.all().update(status=False)
                return Response({'message': 'All orders deleted successfully!'})
        else:
            return HttpResponse(status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    finally:
        # This block will be executed regardless of the try block's outcome.
        # You can put cleanup code here, if needed.
        pass


@api_view(['GET'])
def get_orders_by_user(request, user_id):
    # Get all Order objects related to the user_id
    orders = Order.objects.filter(order_detail__user_id=user_id).order_by('order_detail__time_start')

    paginator = CustomPageNumberPagination()

    result_page = paginator.paginate_queryset(orders, request)

    # If no orders are found, return an empty list
    if not orders.exists():
        return Response([])

    # Serialize the data
    serializer = OrderByUserSerializer(result_page, many=True)

    # Return the serialized data
    return paginator.get_paginated_response(serializer.data)
