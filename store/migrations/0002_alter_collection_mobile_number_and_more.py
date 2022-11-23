# Generated by Django 4.1.3 on 2022-11-20 08:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='mobile_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.MinValueValidator(11), django.core.validators.MaxValueValidator(11)]),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='mobile_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.MinValueValidator(11), django.core.validators.MaxValueValidator(11)]),
        ),
    ]
