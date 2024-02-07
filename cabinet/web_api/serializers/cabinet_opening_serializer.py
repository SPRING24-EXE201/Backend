from rest_framework import serializers


class CabinetOpeningSerializerRequest(serializers.Serializer):
    hash_code = serializers.UUIDField(required=True)
