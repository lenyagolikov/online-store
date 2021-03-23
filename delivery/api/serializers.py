from rest_framework import serializers

from ..models import Courier, Order


class CouriersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'


class OrdersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
