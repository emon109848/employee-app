"""
Serializers for Employee APIs
"""
from rest_framework import serializers

from core.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employee."""

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email',
                  'mobile', 'date_of_birth', 'photo']
        read_only_fields = ['id']


class EmployeeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to employees."""

    class Meta:
        model = Employee
        fields = ['id', 'photo']
        read_only_fields = ['id']
        extra_kwargs = {'photo': {'required': 'True'}}