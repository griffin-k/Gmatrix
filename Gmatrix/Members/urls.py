from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('members_mgt/', views.dashboard_members, name='members'),

    path('members_mgt_view/', views.members_view, name='members_view'),
    path('members_mgt_register/', views.members_register, name='members_register'),
    path('attendence_mgt/', views.dashboard_attendence, name='attendence'),
    path('mark_attendence/', views.mark_attendence, name='mark_atten'),



     path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('check-cnic/', views.check_cnic, name='check_cnic'),


]
