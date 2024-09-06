from django.urls import path
from .views import ProductList, inventory_dashboard, view_inventory, add_product, issue_component

urlpatterns = [
    path('inventory_mgt/', inventory_dashboard, name='inventory_dashboard'),
    path('view_inventory/', view_inventory, name='inventory_view'),
    path('add_products/', add_product, name='product_add'),
    path('api/products/', ProductList.as_view(), name='product_list'),


    path('issue-component/', issue_component, name='issue_component'),
]
