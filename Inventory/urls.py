from django.urls import path
from .views import ProductList, inventory_dashboard, view_inventory, add_product, issue_component, issued_items_view, return_item, update_product, delete_product, view_products

urlpatterns = [
    path('inventory_mgt/', inventory_dashboard, name='inventory_dashboard'),
    path('view_inventory/', view_inventory, name='inventory_view'),
    path('add_products/', add_product, name='product_add'),
    path('api/products/', ProductList.as_view(), name='product_list'),
    path('issued-items/', issued_items_view, name='issued_items'),
    path('return-item/<int:item_id>/', return_item, name='return_item'),



    path('issue-component/', issue_component, name='issue_component'),
    path('update/<int:product_id>/', update_product, name='update_product'),
    path('delete/<int:pk>/', delete_product, name='delete_product'), 



    path('products/', view_products, name='view_products'),
    path('product/<int:product_id>/edit/', update_product, name='update_product'),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),
]
