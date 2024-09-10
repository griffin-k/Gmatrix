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




def application_list_view(request):
    filter_option = request.GET.get('filter', 'all')  
    if filter_option == 'shortlisted':
        applications = MemberApplication.objects.filter(is_shortlisted=True)
    else:
        applications = MemberApplication.objects.all()
    paginator = Paginator(applications, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hiring/application_list.html', {'page_obj': page_obj, 'filter_option': filter_option})




def shortlist_application(request, id):
    application = get_object_or_404(MemberApplication, id=id)
    if request.method == 'POST':
        application.is_shortlisted = True
        application.save()
    return redirect(f"{reverse('application_list')}?success=true")  




def view_hiring_dashboard(request):
    total_applications = MemberApplication.objects.count()
    shortlisted_applications = MemberApplication.objects.filter(is_shortlisted=True).count()

    context = {
        'total_applications': total_applications,
        'shortlisted_applications': shortlisted_applications,
    }
    return render(request, 'hiring/hiring_dashboard.html',context)
