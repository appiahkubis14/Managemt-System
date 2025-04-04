from django.shortcuts import render
from utils import sidebar
from .models import InventoryItem
from employees.models import Employee
from departments.models import Department
from inventory.models import ItemCategory

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import InventoryItem, ItemCategory
from .forms import InventoryItemForm
from inventory.models import InventoryRequest,UniqueInventoryItem
from django.contrib import messages
from django.db import models
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import InventoryTransaction
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json

def inventory_dashboard_view(request):
    inventories = UniqueInventoryItem.objects.all()
    employees = Employee.objects.all()
    departments = Department.objects.filter(name__in=["Transport", "Warehouse", "Procurement & Inventory Management"])
    inventory_request = InventoryRequest.objects.all()

    print(inventories)
    department_config = {
        "Transport": {"icon": "mdi mdi-truck", "color": "danger"},
        "Warehouse": {"icon": "mdi mdi-warehouse", "color": "info"},
        "Procurement & Inventory Management": {"icon": "mdi mdi-buffer", "color": "success"},
    }

#     department_data = [
#     {"name": "Transport", "color": "primary", "icon": "fas fa-truck", "total_employees": 10, "total_inventory": 150, "total_requests": 5},
#     {"name": "Warehouse", "color": "info", "icon": "fas fa-warehouse", "total_employees": 8, "total_inventory": 200, "total_requests": 3},
#     {"name": "Procurement & Inventory Management", "color": "success", "icon": "fas fa-box", "total_employees": 6, "total_inventory": 300, "total_requests": 7},
# ]


    department_data = []
    for department in departments:
        department_data.append({
            "name": department.name,
            "total_inventory": UniqueInventoryItem.objects.filter(department=department).count(),
            "total_employees": Employee.objects.filter(department=department).count(),
            "total_requests": InventoryRequest.objects.filter(to_department=department).count(),
            "icon": department_config[department.name]["icon"],
            "color": department_config[department.name]["color"],
        })

    category_counts = (
        UniqueInventoryItem.objects.values("category")
        .annotate(total_quantity=models.Sum("quantity"))
    )
    total_items = sum(item["total_quantity"] for item in category_counts) or 1  # Avoid division by zero
    category_data = [
        {
            "category": item["category"],
            "percentage": round((item["total_quantity"] / total_items) * 100, 2),
            "color": "primary" if item["category"] == "Category A" else
                     "success" if item["category"] == "Category B" else
                     "warning"
        }
        for item in category_counts
    ]

    monthly_inventory = (
        UniqueInventoryItem.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # 🛠️ Transaction Type Analysis
    transaction_data = (
        InventoryRequest.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month', 'transaction_type')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # 🛠️ Convert transaction data into a format suitable for JavaScript
    transactions_by_month = {}
    for entry in transaction_data:
        month = entry["month"].strftime("%b %Y")
        transaction_type = entry["transaction_type"]
        count = entry["count"]

        if month not in transactions_by_month:
            transactions_by_month[month] = {t_type: 0 for t_type in TransactionType.values}
        transactions_by_month[month][transaction_type] = count

    # Convert to JSON for JavaScript
    transaction_chart_data = json.dumps(transactions_by_month)
    print(transaction_chart_data)

    context = {
        "path": request.path if request.path else "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "inventories": inventories,
        "employees": employees,
        "departments": departments,
        "inventory_request": inventory_request,
        "TransactionType": TransactionType,
        "department_data": department_data,
        "category_data": category_data,
        "monthly_inventory": monthly_inventory,
        "transaction_chart_data": transaction_chart_data,  # 🛠️ Pass chart data to template
    }
    return render(request, "inventory/dashboard.html", context)

####################################################################################################################
from django.utils.text import Truncator

def inventory_view(request):
    inventories = UniqueInventoryItem.objects.all()  # Fetch all inventory items
    categories = ItemCategory.choices
    departments = Department.objects.all()

    # Truncate descriptions to a maximum of 100 characters and add '...more' if necessary
    for item in inventories:
        item.truncated_description = Truncator(item.description).chars(100)  # Truncate description to 100 characters
        if len(item.description) > 50:
            item.truncated_description += '...more'  # Indicate there is more

    context = {
        "path": request.path if request.path else "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "inventories": inventories,  # Pass inventories to the template
        "categories": categories,
        "TransactionType": TransactionType.choices,
        "departments": departments
    }
    return render(request, "inventory/view-inventories.html", context)

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
    return render(request, "inventory/requested-inventories.html", context)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import InventoryRequest

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
def get_inventory_request_detail(request, item_id):
    """Retrieve a specific inventory request by ID"""
    inventory_request = get_object_or_404(InventoryRequest, id=item_id)
    
    data = {
        "id": inventory_request.id,
        "item": inventory_request.item.name if inventory_request.item else None,  # Convert to string
        "category": inventory_request.category,
        "description": inventory_request.description,
        "quantity": inventory_request.quantity,
        "transaction_type": inventory_request.transaction_type,
        "from_department": inventory_request.from_department.name if inventory_request.from_department else None,
        "to_department": inventory_request.to_department.name if inventory_request.to_department else None,
        "employee_name": inventory_request.employee_name,
        "employee_phone": inventory_request.employee_phone,
        "employee_ghana_card_number": inventory_request.employee_ghana_card_number,
        "employee_position": inventory_request.employee_position,
        "created_at": inventory_request.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "remarks": inventory_request.remarks,
    }

    return JsonResponse(data)


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import InventoryItem, Department, Employee, InventoryRequest

@csrf_exempt  # Only needed if CSRF token isn't sent via AJAX
def add_inventory_request(request):
    """Handle creating an inventory request"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data

            # Validate and retrieve item
            item_id = int(data.get("item", 0))
            item = InventoryItem.objects.filter(id=item_id).first()
            if not item:
                return JsonResponse({"status": "error", "message": "Item does not exist"}, status=400)

            # Validate and retrieve departments
            from_department = Department.objects.filter(id=data.get("from_department")).first()
            to_department = Department.objects.filter(id=data.get("to_department")).first()

            # Validate and retrieve employee
            employee = Employee.objects.filter(id=data.get("employee")).first()

            # Create inventory request
            inventory_request = InventoryRequest.objects.create(
                item=item,
                category=data.get("category", ""),
                description=data.get("description", ""),
                quantity=int(data.get("requested_quantity", 0)),
                transaction_type=data.get("transaction_type", "pending"),
                from_department=from_department,
                to_department=to_department,
                employee=employee,
                employee_name=data.get("employee_name", ""),
                employee_phone=data.get("employee_phone", ""),
                employee_ghana_card_number=data.get("employee_ghana_card_number", ""),
                employee_position=data.get("employee_position", ""),
                remarks=data.get("remarks", ""),
            )

            return JsonResponse({"status": "success", "message": "Inventory request added successfully"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def update_inventory_request(request):
    """Handle the update of an inventory request"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inventory_id = data.get('id')

            # Fetch inventory request or return error
            inventory_request = InventoryRequest.objects.get(id=inventory_id)

            # Ensure ForeignKey fields are assigned correctly
            from_department_id = data.get('from_department')
            to_department_id = data.get('to_department')

            inventory_request.item = data.get('item')
            inventory_request.category = data.get('category')
            inventory_request.description = data.get('description')
            inventory_request.quantity = data.get('quantity')
            inventory_request.transaction_type = data.get('transaction_type')

            inventory_request.from_department_id = from_department_id if from_department_id else None
            inventory_request.to_department_id = to_department_id if to_department_id else None

            inventory_request.employee_name = data.get('employee_name').strip() if data.get('employee_name') else ""
            inventory_request.employee_phone = data.get('employee_phone')
            inventory_request.employee_ghana_card_number = data.get('employee_ghana_card_number')
            inventory_request.employee_position = data.get('employee_position')
            inventory_request.remarks = data.get('remarks')

            inventory_request.save()

            return JsonResponse({'status': 'success', 'message': 'Inventory request updated successfully'})

        except InventoryRequest.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Inventory request not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})


@csrf_exempt
def delete_inventory_request(request):
    """Handle delete request for inventory"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inventory_request = InventoryRequest.objects.get(id=data['id'])
            inventory_request.delete()

            return JsonResponse({'status': 'success', 'message': 'Inventory request deleted successfully'})

        except InventoryRequest.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Inventory request not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})


################################################################################################################

from django.shortcuts import render, redirect
from django.http import JsonResponse
from inventory.forms import InventoryItemForm
from inventory.models import InventoryItem, UniqueInventoryItem
from django.db.models import F

from django.http import JsonResponse
import json
from .forms import InventoryItemForm

from django.db.models import F

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import InventoryItem, Department, UniqueInventoryItem

@csrf_exempt
def create_inventory(request):
    """Handle adding multiple inventory items"""
    if request.method == 'POST':
        try:
            # Parse the incoming JSON body
            data = json.loads(request.body)

            # Ensure data is a list
            if not isinstance(data, list):
                return JsonResponse({'status': 'error', 'message': 'Expected a list of inventory items'}, status=400)

            # Iterate over the inventory items in the data
            for item in data:
                # Extract item details
                name = item.get("name")
                category = item.get("category")
                description = item.get("description", "")
                quantity = item.get("quantity")
                reorder_level = item.get("reorder_level")
                department_name = item.get("department")

                # Check for missing required fields
                if not all([name, category, quantity, reorder_level, department_name]):
                    return JsonResponse({'status': 'error', 'message': 'All fields are required for each item'}, status=400)

                # Get the department object
                try:
                    department = Department.objects.get(name=department_name)
                except Department.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f'Department {department_name} does not exist'}, status=400)

                # Create the new InventoryItem
                inventory_item = InventoryItem.objects.create(
                    name=name,
                    category=category,
                    description=description,
                    quantity=quantity,
                    reorder_level=reorder_level,
                    department=department,
                )

                # Check if a UniqueInventoryItem with the same name and category exists
                unique_item = UniqueInventoryItem.objects.filter(name=name).first()

                if unique_item:
                    # Merge the quantities if the UniqueInventoryItem already exists
                    unique_item.quantity += int(quantity)
                    unique_item.save()
                else:
                    # If no existing item, create a new UniqueInventoryItem
                    UniqueInventoryItem.objects.create(
                        name=name,
                        category=category,
                        description=description,
                        quantity=quantity,
                        reorder_level=reorder_level,
                        department=department,
                    )

            return JsonResponse({'status': 'success', 'message': 'Inventory items added successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# def update_or_create_unique_inventory(new_item):
#     """Update or create the corresponding UniqueInventoryItem."""
#     item_key = (new_item.name, new_item.category)  # Check only name and category for uniqueness

#     # Check if the unique item already exists
#     unique_item, created = UniqueInventoryItem.objects.update_or_create(
#         name=new_item.name,
#         category=new_item.category,
#         defaults={
#             'quantity': F('quantity') + new_item.quantity,  # Add quantity to existing
#             'description': new_item.description,
#             'reorder_level': min(new_item.reorder_level, 0),  # Example: use min logic for reorder level
#             'created_at': new_item.created_at
#         }
#     )
#     return unique_item




def get_inventory_by_id(request, item_id):
    """Fetch item details for AJAX request."""
    try:
        # Fetch item details or return 404 if not found
        item = get_object_or_404(UniqueInventoryItem, id=item_id)

        # Return the item details in JSON format
        return JsonResponse({
            "success": True,
            "name": item.name,
            "category": item.category,
            "description": item.description,
            "quantity": item.quantity,
            "reorder_level": item.reorder_level,
            "unit_price": str(item.unit_price),  # Convert DecimalField to string
        })

    except UniqueInventoryItem.DoesNotExist:
        # If the item does not exist, return an error response
        return JsonResponse({"success": False, "error": "Item not found"}, status=404)

    except Exception as e:
        # Catch any other exceptions and return an error message
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def update_inventory(request, item_id):
    """Update an existing inventory item."""
    item = get_object_or_404(InventoryItem, id=item_id)
    
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Inventory updated successfully'}, status=200)
        else:
            # Return form validation errors if the form is invalid
            return JsonResponse({'error': form.errors}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import InventoryItem

@csrf_exempt
def delete_inventory(request, item_id):
    """Delete an inventory item."""
    
    if request.method == 'DELETE':
        # Fetch the item to delete
        item = get_object_or_404(UniqueInventoryItem, id=item_id)
        item.delete()  # Delete the item
        return JsonResponse({'message': 'Inventory deleted successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)




from django.http import JsonResponse
from django.utils import timezone
from inventory.models import UniqueInventoryItem

def inventory_items(request):
    """Fetch unique inventory items as JSON for DataTables."""
    items = UniqueInventoryItem.objects.all().values(
        "id", "name", "category", "quantity", "description", 
        "reorder_level", "created_at", "date_updated"
    )

    for item in items:
        # Convert the created_at and date_updated to the desired format
        item["created_at"] = item["created_at"].astimezone(timezone.get_current_timezone()).strftime('%B %d, %Y, %I:%M %p')
        item["date_updated"] = item["date_updated"].astimezone(timezone.get_current_timezone()).strftime('%B %d, %Y, %I:%M %p')

    return JsonResponse({"data": list(items)})




#######################################################################################################################################
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import InventoryRequest, InventoryItem, TransactionType,UniqueInventoryItem

def update_transaction_type(request, id):
    """Update only the transaction_type of an inventory request."""
    inventory_request = get_object_or_404(InventoryRequest, id=id)

    if request.method == "POST":
        new_transaction_type = request.POST.get("transaction_type")

        if new_transaction_type not in dict(TransactionType.choices).keys():
            messages.error(request, "Invalid transaction type.")
            return redirect("employee_list")  # Redirect back if invalid

        old_transaction_type = inventory_request.transaction_type

        # Start transaction for atomicity
        with transaction.atomic():
            item = inventory_request.item

            # Undo previous transaction effect on stock
            if old_transaction_type in [TransactionType.ISSUED, TransactionType.TRANSFERRED]:
                item.quantity += inventory_request.quantity
            elif old_transaction_type in [TransactionType.RECEIVED, TransactionType.RETURNED]:
                item.quantity -= inventory_request.quantity

            # Apply new transaction type effect on stock
            if new_transaction_type in [TransactionType.ISSUED, TransactionType.TRANSFERRED]:
                if item.quantity < inventory_request.quantity:
                    messages.error(request, "Not enough stock available!")
                    return redirect("employee_list")  # Redirect without saving
                item.quantity -= inventory_request.quantity
            elif new_transaction_type in [TransactionType.RECEIVED, TransactionType.RETURNED]:
                item.quantity += inventory_request.quantity

            # Save changes
            item.save()
            inventory_request.transaction_type = new_transaction_type
            inventory_request.save()

        messages.success(request, "Transaction type updated successfully!")
        return redirect("employee_list")

    return redirect("employee_list")









###########################################################################################################################################@login_required
def process_request(request, id, action):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=403)

    inventory_request = get_object_or_404(InventoryRequest, id=id)
    item = inventory_request.item
    action = action.lower()

    # ✅ Ensure the user has an Employee profile
    approved_by = getattr(request.user, "employee_profile", None)
    if not approved_by:
        return JsonResponse({"success": False, "message": "You don't have an employee profile assigned!"}, status=400)

    print(f"Processing request: ID={id}, Action={action}, Current Type={inventory_request.transaction_type}")

    if action == "approve":
        if item.quantity < inventory_request.quantity:
            return JsonResponse({"success": False, "message": "Not enough stock available!"})

        item.quantity -= inventory_request.quantity
        inventory_request.transaction_type = "APPROVED"
        remarks = "Approved"
        transaction_type = TransactionType.ISSUED

    elif action == "reject":
        inventory_request.transaction_type = "REJECTED"
        remarks = "Rejected"
        transaction_type = TransactionType.REJECTED

    elif action == "abort":
        if inventory_request.transaction_type == "ABORTED":
            return JsonResponse({"success": False, "message": "Request is already aborted!"})

        if inventory_request.transaction_type == "APPROVED":
            item.quantity += inventory_request.quantity
            inventory_request.transaction_type = "ABORTED"
            remarks = "Approval canceled"
            transaction_type = TransactionType.ABORTED
        else:
            return JsonResponse({"success": False, "message": "Only approved requests can be aborted!"})

    else:
        return JsonResponse({"success": False, "message": "Invalid action!"})

    item.save()
    inventory_request.remarks = remarks
    inventory_request.save()

    # ✅ Log the transaction after user verification
    InventoryTransaction.objects.create(
        item=item,
        category=inventory_request.category,
        description=inventory_request.description,
        quantity=inventory_request.quantity,
        transaction_type=transaction_type,
        from_department=inventory_request.from_department,
        to_department=inventory_request.to_department,
        employee=inventory_request.employee,
        approved_by=approved_by,  # Ensure this is set
        approved_at=now(),
        remarks=remarks,
    )

    return JsonResponse({"success": True, "message": f"Request {action}d successfully."})


######################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InventoryItem
from .serializers import InventoryItemSerializer

class BulkInventoryCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        inventory_items = [InventoryItem(**item) for item in data]
        InventoryItem.objects.bulk_create(inventory_items)
        return Response({"status": "success", "message": "Inventory items created successfully!"}, status=status.HTTP_201_CREATED)
