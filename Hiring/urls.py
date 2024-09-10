from django.urls import path
from .views import submit_application,view_hiring_dashboard,application_list_view,shortlist_application,select_application

urlpatterns = [
    path('submit/',submit_application, name='submit_application'),
    path("hiring_dashboard/", view_hiring_dashboard , name="hiring_dashboard"),
    path('applications/', application_list_view, name='application_list'),
    path('applications/select/<int:application_id>/',select_application, name='select_application'),
    path('applications/shortlist/<int:application_id>/', shortlist_application, name='shortlist_application'),

  
]
