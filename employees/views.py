from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee, CustomUser
from .permissions import admin_required, manager_required
from utils import sidebar
from django.contrib import messages
# Admin can update an employee's details
from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmployeeSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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
        "role_choices": role_choices
    }
    return render(request, "employees/employee-list.html", context)

# Manager can view employees in their department
@login_required
@manager_required
def department_employees(request):
    employees = Employee.objects.filter(department=request.user.employee.department)
    return render(request, "employees/department_employees.html", {"employees": employees})



# Admin can add a new employee

def add_employee(request):
    if request.method == "POST":
        # Create the user first
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        selected_role = request.POST.get("role")  # Retrieve role from form

        # Ensure role is valid
        valid_roles = dict(CustomUser.ROLE_CHOICES)
        if selected_role not in valid_roles:
            messages.error(request, "Invalid role selected!")
            return redirect("add_employee")

        # Create the new user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=selected_role  # Assign role
        )

        # Now create the employee record
        employee_name = request.POST.get("employee_name")
        date_of_birth = request.POST.get("date_of_birth")
        date_of_join = request.POST.get("date_of_join")
        gender = request.POST.get("gender")
        ghana_card = request.POST.get("ghana_card")
        phone = request.POST.get("phone")
        photo = request.FILES.get("profile_picture")
        department = request.POST.get("department")
        position = request.POST.get("position")
        hire_date = request.POST.get("hire_date")
        salary = request.POST.get("salary")

        # Check if employee already exists
        if Employee.objects.filter(employee_name=employee_name, date_of_birth=date_of_birth).exists():
            messages.error(request, "Employee already exists!")
            return redirect("add_employee")

        # Create and save the employee
        Employee.objects.create(
            employee_name=employee_name,
            date_of_birth=date_of_birth,
            date_of_join=date_of_join,
            gender=gender,
            ghana_card=ghana_card,
            phone=phone,
            photo=photo,
            user=user,  # Link Employee to the newly created CustomUser
            department=department,
            position=position,
            hire_date=hire_date,
            salary=salary,
        )

        messages.success(request, "Employee and user created successfully!")
        return redirect("employee_list")

   



@login_required
@admin_required
def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == "GET":
        return JsonResponse({
            "employee": {
                "id": employee.id,
                "employee_name": employee.employee_name,
                "department": employee.department,
                "date_of_birth": str(employee.date_of_birth),
                "date_of_join": str(employee.date_of_join),
                "photo": employee.photo.url if employee.photo else None,
                "gender": employee.gender,
                "ghana_card": employee.ghana_card,
                "phone": employee.phone,
                "department": employee.department,
                "position": employee.position,
                "hire_date": str(employee.hire_date),
                "salary": str(employee.salary),
            }
        })

    elif request.method == "POST":
        employee.employee_name = request.POST.get("employee_name", employee.employee_name)
        employee.department = request.POST.get("department", employee.department)
        employee.position = request.POST.get("position", employee.position)
        employee.gender = request.POST.get("gender", employee.gender)
        employee.phone = request.POST.get("phone", employee.phone)
        employee.ghana_card = request.POST.get("ghana_card", employee.ghana_card)
        employee.hire_date = request.POST.get("hire_date", employee.hire_date)
        employee.salary = request.POST.get("salary", employee.salary)

        if "photo" in request.FILES:
            employee.photo = request.FILES["photo"]

        employee.save()
        return JsonResponse({"message": "Employee details updated successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)



import csv
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Employee  # Ensure Employee model exists

# 📤 Export Employees to CSV
def export_employees_csv(request):
    """Exports all employees as a CSV file."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow(["First Name", "Last Name", "Email", "Phone", "Position", "Department", "Hire Date", "Status"])

    employees = Employee.objects.all()
    for employee in employees:
        writer.writerow([
            employee.first_name, 
            employee.last_name, 
            employee.email, 
            employee.phone, 
            employee.position, 
            employee.department, 
            employee.hire_date, 
            employee.status
        ])

    return response

# 📥 Import Employees from CSV
def import_employees(request):
    """Imports employees from a CSV file."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "File is not in CSV format.")
            return redirect('dashboard_employees')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Employee.objects.create(
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email'],
                    phone=row['Phone'],
                    position=row['Position'],
                    department=row['Department'],
                    hire_date=row['Hire Date'],
                    status=row['Status']
                )

            messages.success(request, "Employees imported successfully.")
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")
            
    return redirect('dashboard_employees')



@csrf_exempt  # Remove if using CSRF tokens in JS
@require_http_methods(["DELETE"])  # Only allow DELETE requests
def employee_delete(request, id):
    vehicle = get_object_or_404(Employee, id=id)
    vehicle.delete()
    return JsonResponse({"message": "Vehicle deleted successfully."}, status=200)
