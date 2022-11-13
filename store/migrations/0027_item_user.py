# Generated by Django 4.1.3 on 2022-11-12 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0026_alter_item_cold_price_alter_item_hot_cold_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
