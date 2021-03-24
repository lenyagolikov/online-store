# Generated by Django 3.1.7 on 2021-03-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0010_assign_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assign',
            name='weight',
        ),
        migrations.AddField(
            model_name='courier',
            name='used_weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
