# Generated by Django 4.2.15 on 2024-09-05 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('micro-controller', 'Micro-Controller'), ('sensor', 'Sensor'), ('soldering', 'Soldering'), ('tools', 'Tools')], max_length=50)),
                ('model', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('working', 'Working'), ('damage', 'Damage'), ('out_of_stock', 'Out of Stock')], max_length=50)),
                ('quantity', models.PositiveIntegerField()),
                ('purchase_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
