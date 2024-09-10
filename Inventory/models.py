# models.py

from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
    ('micro-controller', 'Micro-Controller'),
    ('sensor', 'Sensor'),
    ('soldering', 'Soldering'),
    ('tools', 'Tools'),
    ('motor_drivers', 'Motor Drivers'),
    ('communication_modules', 'Communication Modules'),
    ('power_and_charging', 'Power and Charging'),
    ('displays_and_interfaces', 'Displays and Interfaces'),
    ('wiring_and_connectors', 'Wiring and Connectors'),
    ('robotics_and_drones', 'Robotics and Drones'),
    ('miscellaneous', 'Miscellaneous'),
    ('others', 'Others'),
]
    
    STATUS_CHOICES = [
        ('working', 'Working'),
        ('damage', 'Damage'),
        ('out_of_stock', 'Out of Stock'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    model = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.model} ({self.category})"
    




class ComponentIssue(models.Model):
    # Personal Information
    name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=15, unique=True)  # CNIC format: 35201-1234567-8
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()

    # Registration Information
    reg_num = models.CharField(max_length=20)  # Combination of batch_year, dept_degree, and roll_num
    department = models.CharField(max_length=50)
    batch = models.CharField(max_length=10)

    # Component Information
    address = models.CharField(max_length=255)
    component_name = models.CharField(max_length=100)
    issue_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return f'{self.name} - {self.component_name} ({self.cnic})'


    




