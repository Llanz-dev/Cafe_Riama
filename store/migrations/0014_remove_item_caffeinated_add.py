# Generated by Django 4.1.3 on 2022-11-27 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_orderitem_others_add'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='caffeinated_add',
        ),
    ]
