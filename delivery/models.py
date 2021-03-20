from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Courier(models.Model):

    COURIER_TYPES = [
        ('foot', 'foot'),
        ('bike', 'bike'),
        ('car', 'car'),
    ]

    courier_type = models.CharField(max_length=4, choices=COURIER_TYPES)
    regions = ArrayField(ArrayField(models.IntegerField()))
    working_hours = ArrayField(ArrayField(models.CharField(max_length=50)))
    rating = models.FloatField(null=True)
    earnings = models.IntegerField(null=True)


class Order(models.Model):
    weight = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(50)])
    region = models.IntegerField(validators=[MinValueValidator(1)])
    delivery_hours = ArrayField(ArrayField(models.CharField(max_length=50)))


#class Assign(models.Model):
#    courier = models.ForeignKey("Courier", on_delete=models.CASCADE)
#    order = models.ForeignKey("Order", on_delete=models.CASCADE)
#    assign_time = models.DateTimeField(auto_now_add=True)
#    completed_time = models.CharField(max_length=100, blank=True)
