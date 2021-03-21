from rest_framework import serializers
from .models import Courier, Order


class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'


class OrderSieralizer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
