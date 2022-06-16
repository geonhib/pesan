# Generated by Django 4.0.5 on 2022-06-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sacco',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.CharField(choices=[('120000', '120000'), ('240000', '240000')], default=120000, max_length=9),
        ),
    ]