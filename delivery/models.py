from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Courier(models.Model):

    COURIER_TYPES = [
        ('foot', 'foot'),
        ('bike', 'bike'),
        ('car', 'car'),
    ]

    courier_id = models.IntegerField(
        primary_key=True, validators=[MinValueValidator(1)])
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPES)
    regions = ArrayField(models.IntegerField(unique=True,
                                             validators=[MinValueValidator(1)]))
    working_hours = ArrayField(models.CharField(max_length=12, validators=[RegexValidator(
        regex=r'^(([0,1][0-9])|(2[0-3])):[0-5][0-9][-](([0,1][0-9])|(2[0-3])):[0-5][0-9]'
    )]))
    rating = models.FloatField(null=True)
    earnings = models.IntegerField(null=True)


class Order(models.Model):
    order_id = models.IntegerField(
        primary_key=True, validators=[MinValueValidator(1)])
    weight = models.DecimalField(max_digits=5, decimal_places=2,
                                 validators=[MinValueValidator(0.01), MaxValueValidator(50)])
    region = models.IntegerField(validators=[MinValueValidator(1)])
    delivery_hours = ArrayField(models.CharField(max_length=12, validators=[RegexValidator(
        regex=r'^(([0,1][0-9])|(2[0-3])):[0-5][0-9][-](([0,1][0-9])|(2[0-3])):[0-5][0-9]'
    )]))


# class Assign(models.Model):
#    courier = models.ForeignKey("Courier", on_delete=models.CASCADE)
#    order = models.ForeignKey("Order", on_delete=models.CASCADE)
#    assign_time = models.DateTimeField(auto_now_add=True)
#    completed_time = models.CharField(max_length=100, blank=True)
