# Generated by Django 4.1.3 on 2022-11-11 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_alter_item_espresso_shot_alter_item_milk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='cold_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='hot_cold',
            field=models.CharField(choices=[('Hot', 'Hot'), ('Cold', 'Cold')], default='Hot', max_length=5),
        ),
        migrations.AlterField(
            model_name='item',
            name='hot_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='constant/cafe.jpg', upload_to='items-img'),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_slug',
            field=models.SlugField(default=None, unique=True),
        ),
    ]