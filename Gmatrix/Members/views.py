from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import MemberForm
from .models import Member, Attendance
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.http import HttpResponseNotAllowed
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from datetime import date




@login_required
def dashboard_members(request):
    return render(request, 'Members/members_dashboard.html')

def dashboard_attendence(request):
    return render(request, 'Members/attendence_dashboard.html')

# def mark_attendence(request):
#     return render(request, 'Members/mark_attendence.html')



def mark_attendence(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        attendance_type = request.POST.get('attendance_type')
        members = Member.objects.all()
        for member in members:
            present = request.POST.get(f'attendance[{member.id}][Present]', 'off') == 'on'
            absent = request.POST.get(f'attendance[{member.id}][Absent]', 'off') == 'on'
            if present or absent:
                Attendance.objects.update_or_create(
                    member=member,
                    date=date,
                    defaults={'present': present, 'absent': absent, 'type': attendance_type}
                )
        messages.success(request, 'Attendance saved successfully!')
        return redirect('attendance_mark')  # Redirect to a success page or another view

    today = timezone.now().date()
    members = Member.objects.all()
    return render(request, 'Members/mark_attendence.html', {'today': today, 'members': members})








def members_view(request):
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')


    query = Q()

    query &= (Q(name__icontains=search_query) |
              Q(cnic__icontains=search_query) |
              Q(phone_no__icontains=search_query) |
              Q(email__icontains=search_query) |
              Q(designation__icontains=search_query) |
              Q(dept_degree__icontains=search_query))
    
    
    if year_filter:
        year_start, year_end = year_filter.split('-')
        year_start = f'20{year_start}'
        year_end = f'20{year_end}'
        query &= Q(joining_date__year__gte=year_start) & Q(joining_date__year__lte=year_end)

   
    members = Member.objects.filter(query)



    return render(request, 'Members/view_member.html', {
        'members': members,
        'search': search_query,

    })











def members_register(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            print("Form saved successfully")
            return redirect('members_view')  # Redirect to a success page
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    else:
        print("Received GET request")
        form = MemberForm()

    return render(request, 'Members/register_member.html', {'form': form})














###################################
#########   API CALL  #############
###################################


def check_cnic(request):
    if request.method == 'GET':
        cnic = request.GET.get('cnic', '')
        if Member.objects.filter(cnic=cnic).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def delete_member(request, member_id):
    if request.method == 'POST':
        member = get_object_or_404(Member, id=member_id)
        member.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)





