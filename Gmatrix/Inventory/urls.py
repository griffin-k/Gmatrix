

from django.urls import path
from . import views

urlpatterns = [
    path('inventory_mgt/', views.inventory_dashboard, name='inventory_dashboard'),
    path('view_inventory/', views.view_inventory, name='inventory_view'),
    path('add_products/', views.add_product, name='product_add'),
]
