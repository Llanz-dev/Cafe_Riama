# Generated by Django 4.1.3 on 2022-11-30 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_addon_delete_caffeinatedadd_delete_mainadd_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]