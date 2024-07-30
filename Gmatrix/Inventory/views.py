
from django.shortcuts import render



def inventory_dashboard(request):
    return render(request, 'Inventory/inventory_dashboard.html')

def view_inventory(request):
    return render(request, 'Inventory/view_inventory.html')

def add_product(request):
    return render(request, 'Inventory/add_product.html')
