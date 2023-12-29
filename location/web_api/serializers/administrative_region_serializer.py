from rest_framework import serializers
from location.models import AdministrativeRegion


class AdministrativeRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeRegion
        fields = '__all__'

