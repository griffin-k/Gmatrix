from django.shortcuts import render, redirect
from .forms import ProductForm
from django.http import JsonResponse
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from django.contrib import messages
from django.http import HttpResponse
from .forms import ComponentIssueForm
from .models import ComponentIssue
from django.core.paginator import Paginator


def inventory_dashboard(request):
    return render(request, 'Inventory/inventory_dashboard.html')

def view_inventory(request):
    product_list = Product.objects.all()  
    paginator = Paginator(product_list, 10) 
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    context = {
        'page_obj': page_obj, 
    }
    return render(request, 'Inventory/view_inventory.html', context)



def issued_items_view(request):
    issued_items_list = ComponentIssue.objects.all()
    paginator = Paginator(issued_items_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Inventory/return_item.html', {'page_obj': page_obj})

def return_item(request, item_id):
    item = ComponentIssue.objects.get(pk=item_id)
    item.delete()  
    return redirect('issued_items')




def issue_component(request):
    if request.method == 'POST':
        form = ComponentIssueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('issue_component')  
    else:
        form = ComponentIssueForm()
    return render(request, 'Inventory/issue_item.html', {'form': form})









def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_view') 
    else:
        form = ProductForm()
    return render(request, 'Inventory/add_product.html', {'form': form})




class ProductList(APIView):
    def get(self, request):
        category_filter = request.GET.get('category', 'all')
        status_filter = request.GET.get('status', 'all')
        search_term = request.GET.get('search', '').lower()
        products = Product.objects.all()
        if category_filter != 'all':
            products = products.filter(category=category_filter)
        if status_filter != 'all':
            products = products.filter(status=status_filter)
        if search_term:
            products = products.filter(model__icontains=search_term)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
