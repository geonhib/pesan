# Generated by Django 4.0.5 on 2022-06-17 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_package_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sacco',
            name='telephone',
        ),
    ]
