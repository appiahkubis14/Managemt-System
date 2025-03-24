from django.shortcuts import render
from utils import sidebar

# Create your views here.
def warehouse_view(request):

    context = {
        "path": request.path if request.path else "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items
    }
    return render(request, "warehouse/dashboard.html",context)