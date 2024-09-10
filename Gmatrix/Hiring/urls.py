from django.urls import path
from .views import shortlist_application,submit_application,view_hiring_dashboard,application_list_view

urlpatterns = [
    path('submit/',submit_application, name='submit_application'),
    path("hiring_dashboard/", view_hiring_dashboard , name="hiring_dashboard"),
    path('applications/', application_list_view, name='application_list'),

    path('applications/shortlist/<int:id>/', shortlist_application, name='shortlist_application'),
]
