from rest_framework import fields, serializers
from .models import Courier, Order, Assign


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'
