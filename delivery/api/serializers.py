from rest_framework import serializers
from ..models import Courier, Order


class CourierCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
