from django.db import models


class Employee(models.Model):
    """Model of an Employee."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    # photo = models.ImageField(upload_to='employee_photos/')

    def __str__(self) -> str:

        return self.email
