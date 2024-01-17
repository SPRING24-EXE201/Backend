from rest_framework import serializers
class OtpConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()