# Generated by Django 4.0.5 on 2022-06-21 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_trail_updated_on_trail_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trail',
            name='sacco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.sacco'),
        ),
    ]
