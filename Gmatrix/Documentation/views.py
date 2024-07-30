from django.shortcuts import render
from django.contrib.auth.decorators import login_required





@login_required()
def documentation_dashboard(request):
    return render(request, 'Documentation/dashboard_documentation.html')