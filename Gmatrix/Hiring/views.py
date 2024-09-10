from django.shortcuts import render, redirect, get_object_or_404
from .models import MemberApplication
from .forms import MemberApplicationForm
from django.core.paginator import Paginator
from django.urls import reverse


def submit_application(request):
    if request.method == 'POST':
        form = MemberApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application_list')
    else:
        form = MemberApplicationForm()
    return render(request, 'hiring/submit_application.html', {'form': form})


def view_hiring_dashboard(request):
    total_applications = MemberApplication.objects.count()
    shortlisted_applications = MemberApplication.objects.filter(is_shortlisted=True).count()
    context = {
        'total_applications': total_applications,
        'shortlisted_applications': shortlisted_applications,
        'selected_applications': MemberApplication.objects.filter(is_selected=True).count()
    }
    return render(request, 'hiring/hiring_dashboard.html',context)





def application_list_view(request):
    filter_option = request.GET.get('filter', 'all')  
    if filter_option == 'shortlisted':
        applications = MemberApplication.objects.filter(is_shortlisted=True, is_selected=False)
    elif filter_option == 'selected':
        applications = MemberApplication.objects.filter(is_selected=True)
    else:
        applications = MemberApplication.objects.all().order_by('id')
    paginator = Paginator(applications, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hiring/application_list.html', {'page_obj': page_obj, 'filter_option': filter_option})


def select_application(request, application_id):
    application = get_object_or_404(MemberApplication, id=application_id)
    application.is_selected = True
    application.save()
    return redirect('application_list') 




def shortlist_application(request, application_id):
    application = get_object_or_404(MemberApplication, id=application_id)
    application.is_shortlisted = True
    application.save()
    return redirect('application_list')

