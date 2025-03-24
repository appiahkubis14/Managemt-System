from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee, CustomUser
from .permissions import admin_required, manager_required
from utils import sidebar
from django.contrib import messages
# Admin can update an employee's details
from django.http import JsonResponse

# Admin can view all employees
@login_required
@admin_required
def employee_list(request):
    employees = Employee.objects.all()
    sidebar_items = sidebar.Sidebar.sidebar_items
    context={
        "sidebar_items": sidebar_items,
        "employees": employees
    }
    return render(request, "employees/employee-list.html", context)

# Manager can view employees in their department
@login_required
@manager_required
def department_employees(request):
    employees = Employee.objects.filter(department=request.user.employee.department)
    return render(request, "employees/department_employees.html", {"employees": employees})



# Admin can add a new employee
@login_required
@admin_required
def add_employee(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        employee_name = request.POST.get("employee_name")
        date_of_birth = request.POST.get("date_of_birth")
        date_of_join = request.POST.get("date_of_join")
        gender = request.POST.get("gender")
        ghana_card = request.POST.get("ghana_card")
        phone = request.POST.get("phone")
        department = request.POST.get("department")
        position = request.POST.get("position")
        hire_date = request.POST.get("hire_date")
        salary = request.POST.get("salary")

        user = get_object_or_404(CustomUser, id=user_id)

        # Check if employee already exists
        if Employee.objects.filter(user=user).exists():
            messages.error(request, "Employee already exists!")
            return redirect("add_employee")

        Employee.objects.create(
            user=user,
            employee_name=employee_name,
            date_of_birth=date_of_birth,
            date_of_join=date_of_join,
            gender=gender,
            ghana_card=ghana_card,
            phone=phone,
            department=department,
            position=position,
            hire_date=hire_date,
            salary=salary,
            submitted_by=request.user
        )
        messages.success(request, "Employee added successfully!")
        return redirect("employee_list")

    return render(request, "employees/add_employee.html")




@login_required
@admin_required
def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == "GET":
        return JsonResponse({
            "employee": {
                "employee_id": employee.employee_id,
                "employee_name": employee.employee_name,
                "department": employee.department,
                "position": employee.position,
                "gender": employee.gender,
                "phone": employee.phone,
                "ghana_card": employee.ghana_card,
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
