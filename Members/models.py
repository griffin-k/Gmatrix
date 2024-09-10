from django.db import models
from django.utils import timezone



class Member(models.Model):
    CATEGORY_CHOICES = [
        ('Student', 'Student'),
        ('Alumni', 'Alumni'),
    ]

    DEPARTMENT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Software Engineering', 'Software Engineering'),
        ('Information Technology', 'Information Technology'),
    ]

    DESIGNATION_CHOICES = [
    ('President', 'President'),
    ('Vice President', 'Vice President'),
    ('General Secretary', 'General Secretary'),
    ('Information Secretary', 'Information Secretary'),
    ('Finance Secretary', 'Finance Secretary'),
    ('Media Head', 'Media Head'),
    ('Event Head', 'Event Head'),
    ('Documentation Head', 'Documentation Head'),
    ('Member', 'Member'),
    ('Core Member', 'Core Member'),
    ('Lego Advisor', 'Lego Advisor'),
    ('Graphic Designer', 'Graphic Designer'),
    ('Technical Head', 'Technical Head'),
    ('Assistant Technical Head', 'Assistant Technical Head'),
    ('Secretary', 'Secretary'),
    ('Treasurer', 'Treasurer'),
]


    BATCH_CHOICES = [
        ('SP-25', 'SP-25'),
        ('FA-25', 'FA-25'),
        ('SP-24', 'SP-24'),
        ('FA-24', 'FA-24'),
        ('FA-23', 'FA-23'),
        ('SP-23', 'SP-23'),
        ('FA-22', 'FA-22'),
        ('SP-22', 'SP-22'),
        ('FA-21', 'FA-21'),
        ('SP-21', 'SP-21'),
        ('FA-20', 'FA-20'),
        ('SP-20', 'SP-20'),
        ('FA-19', 'FA-19'),
        ('SP-19', 'SP-19'),
        ('FA-18', 'FA-18'),
        ('SP-18', 'SP-18'),
        ('FA-17', 'FA-17'),
        ('SP-17', 'SP-17'),
        ('FA-16', 'FA-16'),
        ('SP-16', 'SP-16'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('On Warning', 'On Warning'),
        ('Terminated', 'Terminated'),
    ]
    
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=15)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()
    batch_year = models.CharField(max_length=10, default='FA-23')
    dept_degree = models.CharField(max_length=10, default='BSCS')
    roll_num = models.CharField(max_length=10, default='000')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    batch = models.CharField(max_length=10, choices=BATCH_CHOICES, default='FA-23')
    address = models.CharField(max_length=255)
    joining_date = models.DateField()
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Inactive')

    def __str__(self):
        return self.name




class Attendance(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=50, default='Regular')  
    present = models.BooleanField(default=False)
    absent = models.BooleanField(default=False)

