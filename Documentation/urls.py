
from django.urls import path
from . import views

urlpatterns = [
    path('documentation_mgt/', views.documentation_dashboard, name='documentation_dashboard'),
]
