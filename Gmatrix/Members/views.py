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

from django.shortcuts import render
from django.utils.timezone import now
from datetime import datetime, timedelta




@login_required
def dashboard_members(request):
    return render(request, 'Members/members_dashboard.html')

def dashboard_attendence(request):
    return render(request, 'Members/attendence_dashboard.html')

# def check_attendance(request):
#     return render(request, 'Members/view_attendence.html')



# def check_attendance(request):
#     search_query = request.GET.get('search', '')
#     start_date = request.GET.get('start_date', '')
#     end_date = request.GET.get('end_date', '')

#     # Set default dates if not provided
#     if not start_date:
#         start_date = datetime.today().strftime('%Y-%m-01')  # First day of the current month
#     if not end_date:
#         end_date = datetime.today().strftime('%Y-%m-%d')  # Today's date

#     # Convert strings to date objects
#     try:
#         start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
#         end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
#     except ValueError:
#         start_date_obj = datetime.today().date().replace(day=1)
#         end_date_obj = datetime.today().date()

#     # Filter Attendance records
#     attendance_records = Attendance.objects.filter(
#         date__range=[start_date_obj, end_date_obj]
#     ).select_related('member')

#     # Aggregate attendance data
#     member_attendance = {}
#     total_present = 0
#     total_absent = 0

#     for record in attendance_records:
#         if record.member not in member_attendance:
#             member_attendance[record.member] = {'present': 0, 'absent': 0}

#         if record.present:
#             member_attendance[record.member]['present'] += 1
#             total_present += 1
#         if record.absent:
#             member_attendance[record.member]['absent'] += 1
#             total_absent += 1

#     members = []
#     for member, attendance in member_attendance.items():
#         total_days = attendance['present'] + attendance['absent']
#         present_percentage = (attendance['present'] / total_days * 100) if total_days else 0
#         absent_percentage = 100 - present_percentage

#         members.append({
#             'name': member.name,
#             'designation': member.designation,
#             'present': attendance['present'],
#             'absent': attendance['absent'],
#             'present_percentage': present_percentage,
#             'absent_percentage': absent_percentage,
#         })

#     context = {
#         'members': members,
#         'search_query': search_query,
#         'start_date': start_date,
#         'end_date': end_date,
#         'total_present': total_present,
#         'total_absent': total_absent,
#     }



#     return render(request, 'Members/view_attendence.html', context)






def check_attendance(request):
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Set default dates if not provided
    if not start_date:
        start_date = datetime.today().strftime('%Y-%m-01')  # First day of the current month
    if not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d')  # Today's date

    # Convert strings to date objects
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        start_date_obj = datetime.today().date().replace(day=1)
        end_date_obj = datetime.today().date()

    # Filter Attendance records based on date range
    attendance_records = Attendance.objects.filter(
        date__range=[start_date_obj, end_date_obj]
    ).select_related('member')

    # Apply search filter if provided
    if search_query:
        attendance_records = attendance_records.filter(
            Q(member__name__icontains=search_query) | Q(member__email__icontains=search_query)
        )

    # Aggregate attendance data
    member_attendance = {}
    total_present = 0
    total_absent = 0

    for record in attendance_records:
        if record.member not in member_attendance:
            member_attendance[record.member] = {'present': 0, 'absent': 0}

        if record.present:
            member_attendance[record.member]['present'] += 1
            total_present += 1
        if record.absent:
            member_attendance[record.member]['absent'] += 1
            total_absent += 1

    members = []
    for member, attendance in member_attendance.items():
        total_days = attendance['present'] + attendance['absent']
        present_percentage = (attendance['present'] / total_days * 100) if total_days else 0
        absent_percentage = 100 - present_percentage

        members.append({
            'name': member.name,
            'designation': member.designation,
            'present': attendance['present'],
            'absent': attendance['absent'],
            'present_percentage': present_percentage,
            'absent_percentage': absent_percentage,
        })

    context = {
        'members': members,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'total_present': total_present,
        'total_absent': total_absent,
    }

    return render(request, 'Members/view_attendence.html', context)









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
            return redirect('members_view')  
        else:
            print("Form is not valid")
            print(form.errors)  
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





