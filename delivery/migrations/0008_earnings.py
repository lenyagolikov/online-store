# Generated by Django 3.1.7 on 2021-03-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_auto_20210326_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='Earnings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courier_id', models.IntegerField()),
                ('courier_type', models.CharField(choices=[('foot', '2'), ('bike', '5'), ('car', '9')], max_length=4)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]