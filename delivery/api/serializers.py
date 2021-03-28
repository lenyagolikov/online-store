from rest_framework import serializers
from datetime import datetime

from .validates import *
from ..models import *


class CouriersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']

    def validate_courier_id(self, data):
        if validate_id(data):
            return data

        raise serializers.ValidationError()

    def validate_regions(self, data):
        if validate_regions(data):
            return data

        raise serializers.ValidationError()

    def validate_working_hours(self, data):
        if validate_hours(data):
            return data

        raise serializers.ValidationError()


class CourierUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']
        read_only_fields = ['courier_id']
        extra_kwargs = {'courier_type': {'required': False}, 'regions': {'required': False},
                        'working_hours': {'required': False},
                        }

    def validate_courier_id(self, data):
        if validate_id(data):
            return data

        raise serializers.ValidationError()

    def validate_region(self, data):
        if validate_region(data):
            return data

        raise serializers.ValidationError()

    def validate_working_hours(self, data):
        if validate_hours(data):
            return data

        raise serializers.ValidationError()


class OrdersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['order_id', 'weight', 'region', 'delivery_hours']

    def validate_order_id(self, data):
        if validate_id(data):
            return data

        raise serializers.ValidationError()

    def validate_weight(self, data):
        if validate_weight(data):
            return data

        raise serializers.ValidationError()

    def validate_region(self, data):
        if validate_region(data):
            return data

        raise serializers.ValidationError()

    def validate_delivery_hours(self, data):
        if validate_hours(data):
            return data

        raise serializers.ValidationError()


class OrdersAssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assign
        fields = ['courier_id']


class OrdersCompleteSerializer(serializers.ModelSerializer):

    courier_id = serializers.IntegerField()
    order_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['courier_id', 'order_id', 'complete_time']

    def validate_complete_time(self, data):
        try:
            datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%fZ')
            return data
        except ValueError:
            raise serializers.ValidationError()
