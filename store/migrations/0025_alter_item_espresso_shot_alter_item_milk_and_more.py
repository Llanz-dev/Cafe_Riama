# Generated by Django 4.1.3 on 2022-11-11 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_alter_item_category_alter_item_cold_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='espresso_shot',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='milk',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='syrup_pump',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='whip_cream',
            field=models.BooleanField(default=False),
        ),
    ]