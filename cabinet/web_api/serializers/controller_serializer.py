from rest_framework import serializers
from cabinet.models import Controller


class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controller
        fields = ['location_id', 'name', 'kafka_id', 'topic', 'status']
