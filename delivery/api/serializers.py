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

        raise serializers.ValidationError(
            "This field must be unique and positive integer number")

    def validate_regions(self, data):
        if validate_regions(data):
            return data

        raise serializers.ValidationError(
            "This field must be an array of unique and positive integer numbers")

    def validate_working_hours(self, data):
        if validate_hours(data):
            return data

        raise serializers.ValidationError(
            "This field must be an array of the strings in the following format: HH:MM-HH:MM")


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

    def validate_regions(self, data):
        if validate_regions(data):
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

        raise serializers.ValidationError(
            "This field must be unique and positive integer number")

    def validate_weight(self, data):
        if validate_weight(data):
            return data

        raise serializers.ValidationError(
            "This field should be between 0.01 and 50")

    def validate_region(self, data):
        if validate_region(data):
            return data

        raise serializers.ValidationError(
            "This field must be positive integer number")

    def validate_delivery_hours(self, data):
        if validate_hours(data):
            return data

        raise serializers.ValidationError(
            "This field must be an array of the strings in the following format: HH:MM-HH:MM")


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

            if len(data) == 23:
                return data

            raise serializers.ValidationError()
        except ValueError:
            raise serializers.ValidationError()
