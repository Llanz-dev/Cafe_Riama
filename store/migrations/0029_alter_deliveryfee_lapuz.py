# Generated by Django 4.1.3 on 2022-12-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_deliveryfee_lapuz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryfee',
            name='lapuz',
            field=models.PositiveSmallIntegerField(default=70),
        ),
    ]
