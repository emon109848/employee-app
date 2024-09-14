"""
URL mappings for the employee app
"""
from django.urls import(
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from employee import views

router = DefaultRouter()
router.register('employee', views.EmployeeViewset)

app_name = 'employee'

urlpatterns = [
    path('', include(router.urls)),
]