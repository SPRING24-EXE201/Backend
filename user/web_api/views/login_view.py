from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from exe201_backend.common.utils import Utils
from user.models import User
from user.web_api.serializers.login_serializer import LoginSerializer


@extend_schema(
    request={'application/json': LoginSerializer}
)
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    status = 400
    data = {}
    if serializer.is_valid():
        try:
            user_exist = User.objects.get(email=serializer.data.get('email'))
            rs = Utils.send_otp(serializer.data.get('email'), 'đăng nhập')
            if rs:
                data = {
                    'Message': 'Đã gửi mail',
                }
                status = 200
        except User.DoesNotExist:
            data = {
                'Message': 'Tài khoản không tồn tại!'
            }
    return Response(status=status, data=data)
