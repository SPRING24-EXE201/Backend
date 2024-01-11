from rest_framework import serializers
from user.models import User
class LoginInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'image_link']