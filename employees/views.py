from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee, CustomUser
from .permissions import admin_required, manager_required
from utils import sidebar
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from inventory.models import InventoryItem,UniqueInventoryItem
from departments.models import Department
from inventory.models import ItemCategory
from django.shortcuts import render, get_object_or_404, redirect
from inventory.models import InventoryRequest
from inventory.models import TransactionType
import csv
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Employee  # Ensure Employee model exists
from transport.models import Driver , DriverAssistant


# Admin can view all employees
@login_required
@admin_required
def employee_list(request):
    employees = Employee.objects.all()
    sidebar_items = sidebar.Sidebar.sidebar_items
    role_choices = CustomUser.ROLE_CHOICES
    context={
        "sidebar_items": sidebar_items,
        "employees": employees,
        "role_choices": role_choices,
        
    }
    return render(request, "employees/employee-list.html", context)

# Manager can view employees in their department
@login_required
@manager_required
def department_employees(request):
    employees = Employee.objects.filter(department=request.user.employee.department)
    return render(request, "employees/department_employees.html", {"employees": employees})


# Admin can add a new employee
# def add_employee(request):
#     if request.method == "POST":
#         # Create the user first
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         selected_role = request.POST.get("role")  # Retrieve role from form

#         # Ensure role is valid
#         valid_roles = dict(CustomUser.ROLE_CHOICES)
#         if selected_role not in valid_roles:
#             messages.error(request, "Invalid role selected!")
#             return redirect("add_employee")

#         # Create the new user
#         user = CustomUser.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             role=selected_role  # Assign role
#         )
#         # Now create the employee record
#         employee_name = request.POST.get("employee_name")
#         date_of_birth = request.POST.get("date_of_birth")
#         date_of_join = request.POST.get("date_of_join")
#         gender = request.POST.get("gender")
#         ghana_card = request.POST.get("ghana_card")
#         phone = request.POST.get("phone")
#         photo = request.FILES.get("profile_picture")
#         department = request.POST.get("department")
#         position = request.POST.get("position")
#         hire_date = request.POST.get("hire_date")
#         salary = request.POST.get("salary")

#         # Check if employee already exists
#         if Employee.objects.filter(employee_name=employee_name, date_of_birth=date_of_birth).exists():
#             messages.error(request, "Employee already exists!")
#             return redirect("add_employee")
#         # Create and save the employee
#         Employee.objects.create(
#             employee_name=employee_name,
#             date_of_birth=date_of_birth,
#             date_of_join=date_of_join,
#             gender=gender,
#             ghana_card=ghana_card,
#             phone=phone,
#             photo=photo,
#             user=user,  # Link Employee to the newly created CustomUser
#             department=department,
#             position=position,
#             hire_date=hire_date,
#             salary=salary,
#         )

#         messages.success(request, "Employee and user created successfully!")
#         return redirect("employee_list")




from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employee, CustomUser

def all_employee_list(request):
    """Fetch all employees for DataTable."""
    employees = Employee.objects.all().values(
        "id", "employee_name", "department", "position", "phone",
        "ghana_card", "hire_date", "salary", "photo"
    )
    return JsonResponse({"data": list(employees)})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employee, CustomUser
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json
# from employees.models import Employee, Driver, DriverAssistant
# from custom_user.models import CustomUser  # Assuming the custom user model is in this app


from django.core.files.storage import FileSystemStorage

@csrf_exempt
def add_employee(request):
    """Create a new employee."""
    if request.method == "POST":
        try:
            # Get the file and form data
            employee_photo = request.FILES.get('profile_picture')  # This gets the uploaded file

            # Get form data from request.POST
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            employee_name = request.POST.get('employee_name')
            date_of_birth = request.POST.get('date_of_birth')
            joining_date = request.POST.get('joining_date')
            gender = request.POST.get('gender')
            ghana_card = request.POST.get('ghana_card')
            phone = request.POST.get('phone')
            phone_2 = request.POST.get('phone_2', '')
            role = request.POST.get('role', 'staff')
            department = request.POST.get('department')
            position = request.POST.get('position')
            license_number = request.POST.get('license_number', '')
            license_expiry_date = request.POST.get('license_expiry_date', '')
            hire_date = request.POST.get('hire_date')
            salary = request.POST.get('salary')

            # Validate required fields
            # required_fields = ["username", "email", "password", "employee_name", "department", "position"]
            # missing_fields = [field for field in required_fields if not locals().get(field)]
            # if missing_fields:
            #     return JsonResponse({"status": "error", "message": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            # Create User
            user = CustomUser.objects.create(username=username, email=email, role=role)
            user.set_password(password)
            user.save()

            # Safely parse dates
            hire_date = parse_date(hire_date) if hire_date else None
            date_of_birth = parse_date(date_of_birth) if date_of_birth else None
            joining_date = parse_date(joining_date) if joining_date else None
            license_expiry_date = parse_date(license_expiry_date) if license_expiry_date else None

            # Create Employee
            employee = Employee.objects.create(
                user=user,
                employee_name=employee_name,
                date_of_birth=date_of_birth,
                date_of_join=joining_date,
                gender=gender,
                department=department,
                position=position,
                phone=phone,
                ghana_card=ghana_card,
                hire_date=hire_date,
                salary=salary,
                photo=employee_photo  # Assign the uploaded file to employee's photo
            )

            # Handle Driver/Driver Assistant Logic
            if user.role.lower() == "driver":
                driver = Driver.objects.create(
                    name=employee_name,
                    ghanacard_number=ghana_card,
                    license_number=license_number,
                    license_expiry_date=license_expiry_date,
                    phone=phone,
                    phone_2=phone_2,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    photo=employee_photo  # Assign photo to driver as well
                )
                employee.driver = driver
                employee.save()

            elif user.role.lower() == "driver_assistant":
                driver_assistant = DriverAssistant.objects.create(
                    name=employee_name,
                    ghanacard_number=ghana_card,
                    phone=phone,
                    phone_2=phone_2,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    photo=employee_photo  # Assign photo to driver assistant as well
                )
                employee.driver_assistant = driver_assistant
                employee.save()

            return JsonResponse({
                "status": "success",
                "message": "Employee added successfully!"
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_employee(request, employee_id):
    """Retrieve details of a specific employee."""
    try:
        employee = get_object_or_404(Employee, id=employee_id)
        user = employee.user  # Access associated User model

        data = {
            "id": employee.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "employee_name": employee.employee_name,
            "date_of_birth": employee.date_of_birth.strftime("%Y-%m-%d") if employee.date_of_birth else "",
            "joining_date": employee.date_of_join.strftime("%Y-%m-%d") if employee.date_of_join else "",
            "gender": employee.gender,
            "ghana_card": employee.ghana_card,
            "phone": employee.phone,
            "phone_2": employee.phone_2,
            "department": employee.department,
            "position": employee.position,
            "hire_date": employee.hire_date.strftime("%Y-%m-%d") if employee.hire_date else "",
            "salary": employee.salary,
            "license_number": "",
            "license_expiry_date": "",
            "profile_picture": employee.photo.url if employee.photo else "",
        }

        # Include license details if the employee is a driver
        if user.role.lower() == "driver" and hasattr(employee, "driver"):
            data["license_number"] = employee.driver.license_number
            data["license_expiry_date"] = (
                employee.driver.license_expiry_date.strftime("%Y-%m-%d")
                if employee.driver.license_expiry_date
                else ""
            )

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)





def requested_inventory(request):
    inventories = InventoryItem.objects.all()  # Fetch all inventory items
    employees = Employee.objects.all()
    departments = Department.objects.all()
    inventory_request = InventoryRequest.objects.all()

    context = {
        "path": request.path if request.path else "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "inventories": inventories,  # Pass inventories to the template
        "employees": employees,
        "departments": departments,
        "inventory_request": inventory_request,
        "TransactionType": TransactionType
    }
    return render(request, "inventory/inventory-request.html", context)


@csrf_exempt
def update_employee(request, id):
    """Update an existing employee."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee = get_object_or_404(Employee, id=id)
            employee.employee_name = data["employee_name"]
            employee.department = data["department"]
            employee.position = data["position"]
            employee.phone = data["phone"]
            employee.ghana_card = data["ghana_card"]
            employee.hire_date = data["hire_date"]
            employee.salary = data["salary"]
            employee.save()
            return JsonResponse({"status": "success", "message": "Employee updated successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
def delete_employee(request, id):
    """Delete an employee."""
    if request.method == "POST":
        try:
            employee = get_object_or_404(Employee, id=id)
            employee.delete()
            return JsonResponse({"status": "success", "message": "Employee deleted successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def requested_inventory(request):
    
    inventories = UniqueInventoryItem.objects.all()  # Fetch all inventory items
    employees = Employee.objects.all()
    departments = Department.objects.all()
    inventory_request = InventoryRequest.objects.all()

    context = {
        "path": request.path if request.path else "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "inventories": inventories,  # Pass inventories to the template
        "employees": employees,
        "departments": departments,
        "inventory_request": inventory_request,
        "TransactionType": TransactionType
    }
    return render(request, "employees/inventory-request.html", context)







###############################################################################################################


def get_inventory_requests(request):
    """Retrieve all inventory requests"""
    inventory_requests = InventoryRequest.objects.all().select_related('item', 'from_department', 'to_department', 'employee')

    data = [
        {
            "id": inv.id,
            "item": inv.item.name,
            "category": inv.category,
            "description": inv.description,
            "quantity": inv.quantity,
            "transaction_type": inv.transaction_type,
            "from_department": inv.from_department.name if inv.from_department else None,
            "to_department": inv.to_department.name if inv.to_department else None,
            "employee_name": inv.employee_name,
            "employee_phone": inv.employee_phone,
            "employee_ghana_card_number": inv.employee_ghana_card_number,
            "employee_position": inv.employee_position,
            "created_at": inv.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": inv.remarks,
        }
        for inv in inventory_requests
    ]

    print(data) 
    return JsonResponse({'data': data})