from rest_framework import serializers

from datetime import datetime, time

from ..models import *


def validate_hours(hours):
    """Проверяет, чтобы введен был верный промежуток

    Если первая часть промежутка больше второй (10:00-08:00), возвращает False
    Если первая часть промежутка меньше второй (10:00-12:00), возвращает True
    """

    for hour in hours:
        start_time = time(int(hour[:2]), int(hour[3:5]))
        end_time = time(int(hour[6:8]), int(hour[9:]))

        if start_time >= end_time:
            return False
    return True


class CouriersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']

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

    def validate_working_hours(self, data):
        if validate_hours(data):
            return data

        raise serializers.ValidationError()


class OrdersCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['order_id', 'weight', 'region', 'delivery_hours']

    def validate_delivery_hours(self, data):
        if validate_hours(data):
            return data

        raise serializers.ValidationError()


class OrdersAssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assign
        fields = ['courier_id']


class OrdersCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assign
        fields = ['courier_id', 'order_id', 'complete_time']

    def validate_complete_time(self, data):
        try:
            datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%fZ')
            return data
        except ValueError:
            raise serializers.ValidationError()
