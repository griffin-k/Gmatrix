from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MemberForm
from .models import Member, Attendance
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect
from rest_framework import generics
from .serializers import AttendanceSerializer
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import MemberSerializer



@login_required
def dashboard_members(request):
    return render(request, 'Members/members_dashboard.html')


@login_required
def dashboard_attendence(request):
    return render(request, 'Members/attendence_dashboard.html')


@login_required
def check_attendance(request):
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

   
    if not start_date:
        start_date = datetime.today().strftime('%Y-%m-01')  
    if not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d') 


    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        start_date_obj = datetime.today().date().replace(day=1)
        end_date_obj = datetime.today().date()


    attendance_records = Attendance.objects.filter(
        date__range=[start_date_obj, end_date_obj]
    ).select_related('member')


    if search_query:
        attendance_records = attendance_records.filter(
            Q(member__name__icontains=search_query) | Q(member__email__icontains=search_query)
        )


    member_attendance = {}
    total_present = 0
    total_absent = 0

    for record in attendance_records:
        member = record.member
        if member not in member_attendance:
            member_attendance[member] = {'present': 0, 'absent': 0}

        if record.present:
            member_attendance[member]['present'] += 1
            total_present += 1
        if record.absent:
            member_attendance[member]['absent'] += 1
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

    paginator = Paginator(members, 10)  # Show 10 members per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'members': page_obj,  # Pass the paginated page object to the template
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'total_present': total_present,
        'total_absent': total_absent,
        'page_obj': page_obj,  # Additional context for page navigation
    }
    return render(request, 'Members/view_attendence.html', context)







@login_required
def mark_attendence(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        attendance_type = request.POST.get('attendance_type')
        active_members = Member.objects.filter(status='Active')
        for member in active_members:
            present = request.POST.get(f'attendance[{member.id}][Present]', 'off') == 'on'
            absent = request.POST.get(f'attendance[{member.id}][Absent]', 'off') == 'on'
            if present or absent:
                Attendance.objects.update_or_create(
                    member=member,
                    date=date,
                    defaults={'present': present, 'absent': absent, 'type': attendance_type}
                )
        messages.success(request, 'Attendance saved successfully!')
        return redirect('attendance_mark') 

    today = timezone.now().date()
    active_members = Member.objects.filter(status='Active')
    return render(request, 'Members/attendance_mark.html', {'today': today, 'members': active_members})









@login_required
def members_view(request):
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')
    status_filter = request.GET.get('status', '')
    query = Q()
    if search_query:
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
    if status_filter:
        query &= Q(status=status_filter)
    members = Member.objects.filter(query).order_by('id')
    paginator = Paginator(members, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Members/view_member.html', {
        'page_obj': page_obj,
        'search': search_query,
        'year_filter': year_filter,
        'status_filter': status_filter,
    })


















@login_required
def members_register(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('members_register')}?success=true")  
        else:
            print(form.errors)
    else:
        form = MemberForm()
    return render(request, 'Members/register_member.html', {'form': form})


@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    form = MemberForm(instance=member)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully.')
            return redirect(f"{reverse('edit_member', kwargs={'member_id': member.id})}?success=true")
    
    return render(request, 'Members/edit_member.html', {'form': form, 'member': member})



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




class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


