# Generated by Django 4.2.5 on 2024-09-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0002_rename_customer_address_customeraddress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerauthentication',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customerauthentication',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
