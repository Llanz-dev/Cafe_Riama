# Generated by Django 4.1.3 on 2022-11-09 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_orderitem_hot_cold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='hot_cold',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
