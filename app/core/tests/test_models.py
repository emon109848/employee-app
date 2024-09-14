"""
Tests for models.
"""
from django.test import TestCase

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_employee(self):
        """Test creating employee is successful"""
        employee = models.Employee.objects.create(
            first_name="SH",
            last_name="Emon",
            email="emon109848@gmail.com",
        )

        self.assertEqual(str(employee), employee.email)
