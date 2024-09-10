from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import shortlisted_members_pdf




urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('Attendence_sheet/', views.generate_Attendence, name='Attendence_sheet'),
    path('student_body/', views.student_body, name='student_body'),
    path('support-center/', views.support_center, name='support_center'),

    path('shortlisted/', shortlisted_members_pdf, name='shorlist_download'),
   

]
