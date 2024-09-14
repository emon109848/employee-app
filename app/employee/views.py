"""
Views for the employee APIs
"""
from rest_framework import viewsets

from core.models import Employee
from employee import serializers


class EmployeeViewset(viewsets.ModelViewSet):
    """View for manage employee APIs"""
    serializer_class = serializers.EmployeeSerializer
    queryset = Employee.objects.all()
