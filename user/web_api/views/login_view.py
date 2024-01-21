from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from exe201_backend.common.utils import Utils
from user.web_api.serializers.login_serializer import LoginSerializer


@extend_schema(
    request={'application/json': LoginSerializer}
)
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        rs = Utils.send_otp(serializer.data.get('email'), 'đăng nhập')
        if rs:
            return Response({
                'Message': 'Đã gửi mail',
            })
    return Response(status=400)
