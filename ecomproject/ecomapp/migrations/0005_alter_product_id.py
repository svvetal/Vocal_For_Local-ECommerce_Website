# Generated by Django 3.2.9 on 2021-11-18 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0004_seller_shop_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False),
        ),
    ]
