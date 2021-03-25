from rest_framework import serializers

from ..models import *


class CouriersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']


class CourierUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']
        read_only_fields = ['courier_id']
        extra_kwargs = {'courier_type': {'required': False}, 'regions': {'required': False},
                        'working_hours': {'required': False},
                        }


class OrdersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['order_id', 'weight', 'region', 'delivery_hours']


class OrdersAssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assign
        fields = ['courier_id']
