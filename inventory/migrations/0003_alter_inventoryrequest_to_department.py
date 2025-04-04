# Generated by Django 5.1.7 on 2025-03-28 04:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_department_alter_inventoryitem_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryrequest',
            name='to_department',
            field=models.ForeignKey(blank=True, default='Inventory', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requests_in', to='inventory.department'),
        ),
    ]
