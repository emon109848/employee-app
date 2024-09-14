"""
Tests for models.
"""
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
