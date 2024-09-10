from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)), 
    path('', include('Authentication.urls')),  
    path('', include('Dashboard.urls')),
    path('', include('Inventory.urls')),
    path('', include('Members.urls')),
    path('', include('Documentation.urls')),
    path('', include('Hiring.urls')),
  

    path("__reload__/", include("django_browser_reload.urls")),

]


