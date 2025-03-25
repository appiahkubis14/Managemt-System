from django.shortcuts import render
from utils import sidebar

# Create your views here.
def inventory_dashboard_view(request):

    context = {
        "path": request.path if request.path else "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items
    }
    return render(request, "inventory/dashboard.html", context)


def inventory_view(request):

    context = {
        "path": request.path if request.path else "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items
    }
    return render(request, "inventory/view-inventories.html", context)


