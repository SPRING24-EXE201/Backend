from rest_framework import serializers
from user.models import User
from cabinet.models import Cell
from order.models import OrderDetail, Assignment
from order.web_api.serializers.assignment_serializer import AssignmentSerializer

class CellSerializer(serializers.ModelSerializer):
    cabinet_description = serializers.SerializerMethodField()
    location_detail = serializers.SerializerMethodField()
    class Meta:
        model = Cell
        fields = ['id', 'cell_index', 'height', 'width', 'depth', 'cabinet_description', 'location_detail']

    def get_cabinet_description(self, obj):
        return obj.cabinet.description if obj.cabinet else None
    def get_location_detail(self, obj):
        return obj.cabinet.controller.location.location_detail if obj.cabinet.controller.location else None

class GetCellAssignmentRequestSerializer(serializers.Serializer):
   cell_id = serializers.IntegerField(required=True)
class GetCellAssignmentResponseSerializer(serializers.ModelSerializer):
    assignees = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = ['assignees', 'user_id', 'email', 'full_name']

    def get_assignees(self, obj):
        filtered_assignees = Assignment.objects.filter(orderDetail__id=obj.id, status=True)
        serializer = AssignmentSerializer(filtered_assignees, many=True)
        return serializer.data

    def get_email(self, obj):
        return obj.user.email if obj.user else None

    def get_full_name(self, obj):
        return obj.user.full_name if obj.user else None

class AssignCellToUserRequestSerializer(serializers.Serializer):
    cell_id = serializers.IntegerField(required=True)
    assignee_email = serializers.EmailField(required=True)
    status = serializers.BooleanField(required=True)


