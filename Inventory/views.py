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
from django.shortcuts import get_object_or_404


def inventory_dashboard(request):
    return render(request, 'Inventory/inventory_dashboard.html')

def view_inventory(request):
    # Retrieve filter parameters from the request
    category_filter = request.GET.get('category', 'all')
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')

    # Start with the base query
    product_list = Product.objects.all()

    # Apply category filter
    if category_filter != 'all':
        product_list = product_list.filter(category=category_filter)

    # Apply status filter
    if status_filter != 'all':
        product_list = product_list.filter(status=status_filter)

    # Apply search filter
    if search_query:
        product_list = product_list.filter(model__icontains=search_query)

    # Order the products
    product_list = product_list.order_by('id')

    # Paginate the results
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare the context for rendering
    context = {
        'page_obj': page_obj,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'search_query': search_query,
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
            messages.success(request, 'Product Added successfully!')
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




def view_products(request):
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if status:
        products = products.filter(status=status)
    if search_query:
        products = products.filter(model__icontains=search_query)
    products = products.order_by('id')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Inventory/view_inventory.html', {'page_obj': page_obj})


def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('view_products') 
    else:
        form = ProductForm(instance=product)
    return render(request, 'Inventory/edit_product.html', {'form': form, 'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('view_products')
    return render(request, 'Inventory/view_inventory.html')