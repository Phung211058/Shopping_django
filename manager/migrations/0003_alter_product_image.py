# Generated by Django 4.2.5 on 2024-09-19 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_rename_quatity_product_quantity_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='products/'),
        ),
    ]
