# Generated by Django 3.2 on 2022-11-03 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
