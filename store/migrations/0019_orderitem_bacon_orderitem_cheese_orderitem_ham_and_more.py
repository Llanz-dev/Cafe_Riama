# Generated by Django 4.1.3 on 2022-11-30 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_pizzadadd_cheese'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='bacon',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='cheese',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='ham',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='pepperoni',
            field=models.BooleanField(default=False),
        ),
    ]
