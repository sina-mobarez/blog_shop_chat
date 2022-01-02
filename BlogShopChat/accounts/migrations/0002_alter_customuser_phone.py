# Generated by Django 3.2.9 on 2022-01-01 15:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format +989999999999. Up to 10 digits allowed.', regex='^(\\+98?)?{?(0?9[0-9]{9,9}}?)$')], verbose_name='Phone number'),
        ),
    ]
