# Generated by Django 4.0.5 on 2022-06-16 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_sacco_options_alter_package_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='capacity',
            field=models.PositiveIntegerField(),
        ),
    ]
