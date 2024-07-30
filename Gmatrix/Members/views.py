from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



@login_required
def dashboard_members(request):
    return render(request, 'Members/members_dashboard.html')

def dashboard_attendence(request):
    return render(request, 'Members/attendence_dashboard.html')

def mark_attendence(request):
    return render(request, 'Members/mark_attendence.html')

def members_view(request):
    return render(request, 'Members/view_member.html')

def members_register(request):
    return render(request, 'Members/register_member.html')
