# Generated by Django 5.0.6 on 2024-09-16 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0005_remove_product_stock_productstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(default='$', max_length=255),
        ),
    ]
