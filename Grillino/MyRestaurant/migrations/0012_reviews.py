# Generated by Django 4.2.17 on 2024-12-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyRestaurant', '0011_customuser_address_customuser_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=100)),
                ('rating', models.IntegerField()),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
