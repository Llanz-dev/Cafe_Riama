# Generated by Django 4.1.3 on 2022-11-10 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_alter_item_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='price',
            new_name='hot_cold',
        ),
    ]