from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['category', 'name', 'cnic', 'phone_no', 'email', 'batch_year', 'dept_degree', 'roll_num', 'department', 'batch', 'address', 'joining_date', 'designation']
    
 
