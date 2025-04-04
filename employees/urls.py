from django.urls import path
from .views import *

urlpatterns = [
    path('employee-list/', employee_list, name='employee_list'),  # Admin View
    path('all-employee-list/', all_employee_list, name='inventory_request'),
    path('department/', department_employees, name='department_employees'),  # Manager View
    path('add/', add_employee, name='add_employee'),  # Admin can add employees
    path("update/<str:id>/", update_employee, name="update_employee"), 
    path("employee-delete/<str:id>/", delete_employee, name="delete_employee"),
    path("all-request-inventory/", get_inventory_requests , name="request-inventory") ,
    # path('inventory-request/',requested_inventory,name='requested_inventory'),
    path("requested-inventory/", requested_inventory , name="inventory-request") ,
    # path('export/', export_employees_csv, name='export_employees_csv'),
    # path('import/', import_employees, name='import_employees'),

    path("employee/<int:employee_id>/", get_employee, name="get_employee"),
    path("employee/<int:employee_id>/update/", update_employee, name="update_employee"),
    path("employee/<int:employee_id>/delete/", delete_employee, name="delete_employee"),
]
