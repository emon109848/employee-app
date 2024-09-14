"""
Tests for employee APIs.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Employee

from employee.serializers import EmployeeSerializer

import datetime
import tempfile
import os

from PIL import Image


EMPLOYEES_URL = reverse('employee:employee-list')


def image_upload_url(employee_id):
    """Create and return a image upload url."""
    return reverse('employee:employee-upload-image', args=[employee_id])

def create_employee(**params):
    """Create and return a sample Employee"""
    defaults = {
        'first_name': 'SH',
        'last_name': 'Emon',
        'email': 'emon109848@gmail.com',
        'mobile': '01674758661',
        'date_of_birth': datetime.date(1990, 1, 1),
    }
    defaults.update(params)

    employee = Employee.objects.create(**defaults)
    return employee


class EmployeeAPITests(TestCase):
    """Test API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_retrive_employee(self):
        """Test retrieving a list of employees."""
        create_employee()
        create_employee()

        res = self.client.get(EMPLOYEES_URL)

        employees = Employee.objects.all().order_by('-id')
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i, employee_data in enumerate(serializer.data):
            self.assertEqual(res.data[i]['first_name'],
                             employee_data['first_name'])
            self.assertEqual(res.data[i]['last_name'],
                             employee_data['last_name'])
            self.assertEqual(res.data[i]['email'], employee_data['email'])
            self.assertEqual(res.data[i]['mobile'], employee_data['mobile'])


class ImageUploadTests(TestCase):
    """Test for image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.employee = create_employee()

    def tearDown(self):
        self.employee.photo.delete()

    def test_upload_image(self):
        """Test uploading an image to an employee."""
        url = image_upload_url(self.employee.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10,10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'photo': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.employee.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('photo', res.data)
        self.assertTrue(os.path.exists(self.employee.photo.path))

    def test_upload_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.employee.id)
        payload = {'photo': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
