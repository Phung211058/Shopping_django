# Generated by Django 4.2.5 on 2024-09-18 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.CharField(max_length=20)),
                ('quatity', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='static/images/')),
            ],
        ),
    ]
