# Generated by Django 5.1.3 on 2024-11-14 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(db_index=True, max_length=17, unique=True)),
                ('manufacturer_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('horse_power', models.IntegerField()),
                ('model_name', models.CharField(max_length=100)),
                ('model_year', models.IntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fuel_type', models.CharField(max_length=50)),
            ],
        ),
    ]
