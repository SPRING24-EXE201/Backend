from rest_framework import serializers

class CabinetOpeningSerializerRequest(serializers.Serializer):
    hash_code = serializers.CharField(max_length=100)

class CabinetOpeningSerializerResponse(serializers.Serializer):
    controller_id = serializers.IntegerField()
    cabinet_id = serializers.IntegerField()
    cell_index = serializers.IntegerField()
