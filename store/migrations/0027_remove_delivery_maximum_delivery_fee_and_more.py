# Generated by Django 4.1.3 on 2022-12-16 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_delivery_maximum_delivery_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='maximum_delivery_fee',
        ),
        migrations.AddField(
            model_name='deliveryfee',
            name='maximum_delivery_fee',
            field=models.PositiveIntegerField(default=300),
        ),
    ]
