# Generated by Django 3.2.9 on 2022-01-06 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20220105_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='description',
            field=models.TextField(default=2021),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='order_number',
            field=models.CharField(blank=True, max_length=23),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
    ]