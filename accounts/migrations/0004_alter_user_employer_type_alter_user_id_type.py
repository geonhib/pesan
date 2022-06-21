# Generated by Django 4.0.5 on 2022-06-21 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_id_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='employer_type',
            field=models.CharField(blank=True, choices=[('self-employment', 'self-employment'), ('organization', 'organization')], default='organization', max_length=60),
        ),
        migrations.AlterField(
            model_name='user',
            name='id_type',
            field=models.CharField(blank=True, choices=[('national ID', 'national'), ('passport', 'passport'), ('other', 'other')], default='national', max_length=20),
        ),
    ]
