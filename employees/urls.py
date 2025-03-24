from django.urls import path
from .views import *

urlpatterns = [
    path('employee-list/', employee_list, name='employee_list'),  # Admin View
    path('employees/department/', department_employees, name='department_employees'),  # Manager View
    path('employees/add/', add_employee, name='add_employee'),  # Admin can add employees
    path("employees/add/", add_employee, name="add_employee"),  # Admin add employee
    path("employees/update/<str:employee_id>/", update_employee, name="update_employee"), 
    
    path('export/', export_employees_csv, name='export_employees_csv'),
    path('import/', import_employees, name='import_employees'),
]
