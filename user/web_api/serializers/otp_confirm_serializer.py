from rest_framework import serializers


class OtpConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(max_value=999999, min_value=100000)