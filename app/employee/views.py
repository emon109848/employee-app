"""
Views for the employee APIs
"""
from rest_framework import (
    viewsets,
    status,
    filters,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
)

from core.models import Employee
from employee import serializers

from PIL import Image
import io


class EmployeeFilter(FilterSet):
    """Custom filter for Employee model to support partial filtering."""
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')
    mobile = CharFilter(field_name='mobile', lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email',
                  'mobile', 'date_of_birth']


class EmployeeViewSet(viewsets.ModelViewSet):
    """View for manage employee APIs"""
    serializer_class = serializers.EmployeeSerializer
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    ordering_fields = ['first_name', 'last_name', 'email',
                       'mobile', 'date_of_birth']

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'upload_image':
            return serializers.EmployeeImageSerializer
        return serializers.EmployeeSerializer

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to Employee."""
        employee = self.get_object()
        serializer = self.get_serializer(employee, data=request.data)

        if 'photo' not in request.FILES:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        image = request.FILES['photo']

        image_size_kb = image.size / 1024
        max_size_kb = 200

        if image_size_kb > max_size_kb:
            image_file = Image.open(image)

            if image_file.mode in ('RGBA', 'LA') and image_file.info.get('transparency') is not None:  # noqa
                image_file = image_file.convert('RGB')

            output_io = io.BytesIO()
            image_file.save(output_io, format='JPEG', quality=85)

            compressed_image = io.BytesIO(output_io.getvalue())
            compressed_image.name = image.name  # Preserve original file name

            request.FILES['photo'] = compressed_image

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
