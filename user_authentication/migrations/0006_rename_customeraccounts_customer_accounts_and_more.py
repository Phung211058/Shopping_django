# Generated by Django 4.2.5 on 2024-09-25 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('user_authentication', '0005_rename_customerauthentication_customeraccounts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerAccounts',
            new_name='Customer_Accounts',
        ),
        migrations.RenameModel(
            old_name='CustomerAddress',
            new_name='Customer_Address',
        ),
    ]
