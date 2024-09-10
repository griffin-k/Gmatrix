# models.py

from django.db import models

class MemberApplication(models.Model):
    name = models.CharField(max_length=255)
    cnic = models.CharField(max_length=15)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()
    reg_num = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    batch = models.CharField(max_length=10)
    address = models.TextField()
    joining_date = models.DateField()
    is_shortlisted = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.name} - {self.reg_num}"


