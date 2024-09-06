# forms.py
from django import forms
from .models import Product,ComponentIssue


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'model', 'status', 'quantity', 'purchase_date', 'price']




class ComponentIssueForm(forms.ModelForm):
    class Meta:
        model = ComponentIssue
        fields = ['name', 'cnic', 'phone_no', 'email', 'reg_num', 'department', 'batch', 'address', 'component_name', 'issue_date', 'return_date']
