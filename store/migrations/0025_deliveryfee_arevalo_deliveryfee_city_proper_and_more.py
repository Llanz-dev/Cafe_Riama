# Generated by Django 4.1.3 on 2022-12-16 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_deliveryfee_alter_delivery_districts'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryfee',
            name='arevalo',
            field=models.PositiveSmallIntegerField(default=70),
        ),
        migrations.AddField(
            model_name='deliveryfee',
            name='city_proper',
            field=models.PositiveSmallIntegerField(default=60),
        ),
        migrations.AddField(
            model_name='deliveryfee',
            name='jaro',
            field=models.PositiveSmallIntegerField(default=50),
        ),
        migrations.AddField(
            model_name='deliveryfee',
            name='la_paz',
            field=models.PositiveSmallIntegerField(default=60),
        ),
        migrations.AddField(
            model_name='deliveryfee',
            name='mandurriao',
            field=models.PositiveSmallIntegerField(default=40),
        ),
        migrations.AddField(
            model_name='deliveryfee',
            name='molo',
            field=models.PositiveSmallIntegerField(default=70),
        ),
    ]