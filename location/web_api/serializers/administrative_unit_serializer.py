from rest_framework import serializers
from location.models import AdministrativeUnit


class AdministrativeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeUnit
        fields = '__all__'

