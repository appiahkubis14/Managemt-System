from django.urls import path
from .views import *

urlpatterns = [
    path('employee-list/', employee_list, name='employee_list'),  # Admin View
    path('all-employee-list/', all_employee_list, name='inventory_request'),
    path('department/', department_employees, name='department_employees'),  # Manager View
    path('add/', add_employee, name='add_employee'),  # Admin can add employees
    path("update/<str:id>/", update_employee, name="update_employee"), 
    path("employee-delete/<str:id>/", delete_employee, name="delete_employee"),
    # path("all-request-inventory/", requested_inventory , name="request-inventory") ,
    path('inventory-request/',requested_inventory,name='requested_inventory'),
    # path('export/', export_employees_csv, name='export_employees_csv'),
    # path('import/', import_employees, name='import_employees'),

    # path('requests/create/', create_inventory_request, name='create_inventory_request'),
#     path('requests/update/<int:request_id>/', update_inventory_request, name='update_inventory_request'),
#     path('requests/delete/<int:request_id>/', delete_inventory_request, name='delete_inventory_request'),

]
