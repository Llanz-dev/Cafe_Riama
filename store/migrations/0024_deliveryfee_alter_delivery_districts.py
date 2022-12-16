# Generated by Django 4.1.3 on 2022-12-16 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_item_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='delivery',
            name='districts',
            field=models.CharField(choices=[('Arevalo', 'Arevalo'), ('City Proper', 'City Proper'), ('Jaro', 'Jaro'), ('La Paz', 'La Paz'), ('Lapuz', 'Lapuz'), ('Mandurriao', 'Mandurriao'), ('Molo', 'Molo')], default='Arevalo', max_length=11),
        ),
    ]
