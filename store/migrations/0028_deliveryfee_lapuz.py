# Generated by Django 4.1.3 on 2022-12-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_remove_delivery_maximum_delivery_fee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryfee',
            name='lapuz',
            field=models.PositiveSmallIntegerField(default=60),
        ),
    ]
