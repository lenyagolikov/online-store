from rest_framework.decorators import api_view
from .serializers import CourierSerializer, OrderSerializer
from .api import data_is_valid


@api_view(['POST'])
def couriers_list(request):
    return data_is_valid(request, CourierSerializer, "couriers")


@api_view(['POST'])
def orders_list(request):
    return data_is_valid(request, OrderSerializer, "orders")
