from django.db import models


class Courier(models.Model):
    courier_type = models.CharField(max_length=20)
    regions = models.CharField(max_length=50)
    working_hours = models.CharField(max_length=100)
    rating = models.FloatField(null=True)
    earnings = models.IntegerField(null=True)


class Order(models.Model):
    weight = models.FloatField()
    region = models.IntegerField()
    delivery_hours = models.CharField(max_length=100)


class Assign(models.Model):
    courier = models.ForeignKey("Courier", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    assign_time = models.DateTimeField(auto_now_add=True)
    completed_time = models.CharField(max_length=100, blank=True)
