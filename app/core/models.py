from django.db import models

import uuid
import os


def employee_image_file_path(instance, filename):
    """Generate file path for new employee image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'employee', filename)


class Employee(models.Model):
    """Model of an Employee."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    photo = models.ImageField(null=True, upload_to=employee_image_file_path)

    def __str__(self) -> str:

        return self.email
