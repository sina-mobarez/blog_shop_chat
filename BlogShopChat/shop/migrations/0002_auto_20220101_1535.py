# Generated by Django 3.2.9 on 2022-01-01 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='type',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='slug'),
        ),
    ]
