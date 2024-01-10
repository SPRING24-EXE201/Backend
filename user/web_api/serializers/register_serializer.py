from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
