# Generated by Django 5.1.7 on 2025-03-30 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_inventoryitem_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryrequest',
            name='transaction_type',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Issued', 'Issued'), ('Received', 'Received'), ('Returned', 'Returned'), ('Transferred', 'Transferred')], max_length=20),
        ),
        migrations.AlterField(
            model_name='inventorytransaction',
            name='transaction_type',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Issued', 'Issued'), ('Received', 'Received'), ('Returned', 'Returned'), ('Transferred', 'Transferred')], max_length=20),
        ),
    ]
