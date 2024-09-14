"""
Tests for models.
"""
from unittest.mock import patch

from django.test import TestCase

from core import models

import datetime


class ModelTests(TestCase):
    """Test models."""

    def test_create_employee(self):
        """Test creating employee is successful"""
        employee = models.Employee.objects.create(
            first_name="SH",
            last_name="Emon",
            email="emon109848@gmail.com",
            date_of_birth=datetime.date(1998, 1, 1)
        )

        self.assertEqual(str(employee), employee.email)

    @patch('core.models.uuid.uuid4')
    def test_employee_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.employee_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/employee/{uuid}.jpg')