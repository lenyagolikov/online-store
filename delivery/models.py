from django.contrib.postgres.fields import ArrayField
from django.db import models


class Courier(models.Model):

    COURIER_TYPES = [
        ('foot', '10'),
        ('bike', '15'),
        ('car', '50'),
    ]

    courier_id = models.IntegerField(primary_key=True)
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPES)
    regions = ArrayField(models.IntegerField())
    working_hours = ArrayField(models.CharField(max_length=12))
    rating = models.FloatField(null=True, default=0)
    earnings = models.IntegerField(null=True, default=0)


class Order(models.Model):

    order_id = models.IntegerField(primary_key=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    region = models.IntegerField()
    delivery_hours = ArrayField(models.CharField(max_length=12))
    is_available = models.BooleanField(default=True)
    complete_time = models.CharField(max_length=24, null=True, default=None)


class Assign(models.Model):

    COURIER_TYPES = [
        ('foot', '2'),
        ('bike', '5'),
        ('car', '9'),
    ]

    courier_id = models.ForeignKey("Courier", on_delete=models.CASCADE)
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPES)
    active_orders = ArrayField(models.IntegerField())
    finished_orders = ArrayField(
        models.IntegerField(), null=True, default=list)
    assign_time = models.CharField(max_length=24, null=True, default=None)
    completed = models.BooleanField(default=False)
