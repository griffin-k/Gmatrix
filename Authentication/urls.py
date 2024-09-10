from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import run_command_view, terminal_view


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('terminal/', terminal_view, name='terminal_view'),  # URL for rendering the terminal page
    path('run-command/', run_command_view, name='run_command_view'),  
]
