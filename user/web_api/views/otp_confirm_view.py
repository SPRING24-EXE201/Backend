from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

from exe201_backend import settings
from user.web_api.serializers.otp_confirm_serializer import OtpConfirmSerializer

from user.models import User

@extend_schema(
    request=OtpConfirmSerializer
)
@api_view(['POST'])
def otp_confirm(request):
    data = {}
    status_code = 200
    try:
        serializers = OtpConfirmSerializer(data=request.data)
        if serializers.is_valid():
            email = serializers.data.get('email')
            otp = serializers.data.get('otp')
            user = authenticate(email=email, otp=otp)
            if user is not None:
                login(request=request, backend=settings.AUTHENTICATION_BACKENDS[0], user=user)
                refresh = RefreshToken.for_user(user)
                data = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
                status_code = 200
                user.refresh_token = str(refresh)
                user.save()
    except User.DoesNotExist as e:
        data = {'message': "Email không tồn tại"}
        status_code = 400
    return JsonResponse(data, status=status_code)

  