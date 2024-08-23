from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import edit_member
from .views import MemberListCreateView, MemberDetailView

urlpatterns = [
    path('members_mgt/', views.dashboard_members, name='members'),

    path('members_mgt_view/', views.members_view, name='members_view'),
    path('members_mgt_register/', views.members_register, name='members_register'),
    path('attendence_mgt/', views.dashboard_attendence, name='attendence'),
    path('attendence_get/', views.mark_attendence, name='attendance_mark'),
    path('view-attendance/', views.check_attendance, name='attendance_view'),
    path('edit-member/<int:member_id>/', edit_member, name='edit_member'),

 
    




     path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('check-cnic/', views.check_cnic, name='check_cnic'),



######### Rest API URLS ##########

##################################

 

    path('members_api/', MemberListCreateView.as_view(), name='member-list-create'),
    path('members_api/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),


]
