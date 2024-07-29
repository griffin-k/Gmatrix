from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



@login_required
def dashboard_view(request):
    return render(request, 'Dashboard/dashboard.html')
