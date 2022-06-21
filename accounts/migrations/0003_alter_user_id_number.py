# Generated by Django 4.0.5 on 2022-06-20 14:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_employer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(14)]),
        ),
    ]