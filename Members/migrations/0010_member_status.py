# Generated by Django 5.0.7 on 2024-08-23 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0009_attendance_type_alter_attendance_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('On Warning', 'On Warning'), ('Terminated', 'Terminated')], default='Inactive', max_length=20),
        ),
    ]
