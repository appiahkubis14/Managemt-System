from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils import sidebar

@login_required
def dashboard_view(request):

    context = {
        "path": request.path if request.path else "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items
    }

    return render(request, "dashboard/dashboard-index.html", context)



def login(request):
    return render(request, "account/login.html")






