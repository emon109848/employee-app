"""
Tests for employee APIs.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Employee

from employee.serializers import EmployeeSerializer


EMPLOYEES_URL = reverse('employee:employee-list')


def create_employee(**params):
    """Create and return a sample Employee"""
    defaults = {
        'first_name': 'SH',
        'last_name': 'Emon',
        'email': 'emon109848@gmail.com',
        'mobile': '01674758661'
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
            self.assertEqual(res.data[i]['first_name'], employee_data['first_name'])
            self.assertEqual(res.data[i]['last_name'], employee_data['last_name'])
            self.assertEqual(res.data[i]['email'], employee_data['email'])
            self.assertEqual(res.data[i]['mobile'], employee_data['mobile'])