from rest_framework.decorators import api_view
from rest_framework.response import Response

from cabinet.models import Controller
from cabinet.web_api.serializers.controller_serializer import ControllerSerializer


@api_view(['GET'])
def get_controller(request):
    """
    Get all controller
    """
    controller = []
    try:
        controller = Controller.objects.all().filter(status=True)
    except Controller.DoesNotExist:
        pass

    data = ControllerSerializer(controller, many=True).data

    return Response({
        'success': True,
        'data': data,
    })
