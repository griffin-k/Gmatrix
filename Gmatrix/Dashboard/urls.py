from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('Attendence_sheet/', views.generate_Attendence, name='Attendence_sheet'),
    path('student_body/', views.student_body, name='student_body'),
   

]
