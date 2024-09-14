"""
Views for the employee APIs
"""
from rest_framework import (
    viewsets,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Employee
from employee import serializers


class EmployeeViewSet(viewsets.ModelViewSet):
    """View for manage employee APIs"""
    serializer_class = serializers.EmployeeSerializer
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'upload_image':
            return serializers.EmployeeImageSerializer
        return serializers.EmployeeSerializer
        
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to Emplyee."""
        employee = self.get_object()
        serializer = self.get_serializer(employee, data=request.data)

        if 'photo' not in request.FILES:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
