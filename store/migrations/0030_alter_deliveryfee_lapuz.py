# Generated by Django 4.1.3 on 2022-12-16 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_alter_deliveryfee_lapuz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryfee',
            name='lapuz',
            field=models.PositiveSmallIntegerField(default=80),
        ),
    ]