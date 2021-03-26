from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Courier(models.Model):

    COURIER_TYPES = [
        ('foot', '10'),
        ('bike', '15'),
        ('car', '50'),
    ]

    courier_id = models.IntegerField(
        primary_key=True, validators=[MinValueValidator(1)])
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPES)
    regions = ArrayField(models.IntegerField(
        validators=[MinValueValidator(1)]))
    working_hours = ArrayField(models.CharField(max_length=12, validators=[RegexValidator(
        regex=r"^(([0,1][0-9])|(2[0-3])):[0-5][0-9][-](([0,1][0-9])|(2[0-3])):[0-5][0-9]"
    )]))
    rating = models.FloatField(null=True)
    earnings = models.IntegerField(null=True)


class Order(models.Model):
    order_id = models.IntegerField(
        primary_key=True, validators=[MinValueValidator(1)])
    weight = models.DecimalField(max_digits=5, decimal_places=2,
                                 validators=[MinValueValidator(Decimal("0.01")), MaxValueValidator(50)])
    region = models.IntegerField(validators=[MinValueValidator(1)])
    delivery_hours = ArrayField(models.CharField(max_length=12, validators=[RegexValidator(
        regex=r'^(([0,1][0-9])|(2[0-3])):[0-5][0-9][-](([0,1][0-9])|(2[0-3])):[0-5][0-9]'
    )]))
    is_available = models.BooleanField(default=True)


class Assign(models.Model):
    courier_id = models.ForeignKey("Courier", on_delete=models.CASCADE)
    order_id = models.ForeignKey("Order", on_delete=models.CASCADE)
    assign_time = models.CharField(max_length=24, null=True, default=None)
    complete_time = models.CharField(max_length=24, null=True, default=None)
