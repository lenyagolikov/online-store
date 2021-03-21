# Generated by Django 3.1.7 on 2021-03-21 15:06

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20210321_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='working_hours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex='^(([0,1][0-9])|(2[0-3])):[0-5][0-9][-](([0,1][0-9])|(2[0-3])):[0-5][0-9]')]), size=None),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_hours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex='^(([0,1][0-9])|(2[0-3])):[0-5][0-9][-](([0,1][0-9])|(2[0-3])):[0-5][0-9]')]), size=None),
        ),
    ]
