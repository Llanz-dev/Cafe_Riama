# Generated by Django 4.1.3 on 2022-12-22 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_remove_favoriteitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoriteitem',
            name='aligue_platter',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='bacon',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='bottled_water',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='cheese',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='espresso_shot',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='ham',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='hot_or_cold',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='milk',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='pepperoni',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='plain_rice',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='rice_platter',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='syrup_pump',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='whip_cream',
        ),
    ]