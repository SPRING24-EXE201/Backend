from rest_framework import serializers
from cabinet.models import Controller


class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controller
        fields = ['id', 'name', 'description', 'status', 'image_link', 'ip_address', 'port', 'username', 'password']
