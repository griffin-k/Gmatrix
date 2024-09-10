# forms.py
from django import forms
from .models import MemberApplication  # Assuming you're saving to a Member model

class MemberApplicationForm(forms.ModelForm):
    class Meta:
        model = MemberApplication  # Replace with your model name
        fields = ['name', 'cnic', 'phone_no', 'email', 'reg_num', 'department', 'batch', 'address', 'joining_date']
