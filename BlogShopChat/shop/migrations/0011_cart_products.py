# Generated by Django 3.2.9 on 2022-01-12 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_product_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='shop.CartItem', to='shop.Product', verbose_name='product of this basket'),
        ),
    ]
