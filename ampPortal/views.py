from django.shortcuts import render

# Create your views here.

def tracking_view(request):
    return render(request, 'ampPortal/dashboard.html')