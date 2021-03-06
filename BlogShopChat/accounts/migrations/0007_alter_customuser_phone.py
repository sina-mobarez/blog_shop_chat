# Generated by Django 3.2.10 on 2022-01-23 15:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customuser_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format +989999999999. Up to 10 digits allowed.', regex='^9\\d{9}$')], verbose_name='Phone number'),
        ),
    ]
