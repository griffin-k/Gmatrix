# Generated by Django 4.2.15 on 2024-09-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hiring', '0003_delete_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberapplication',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
    ]
