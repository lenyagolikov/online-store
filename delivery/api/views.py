from rest_framework.decorators import api_view

from .serializers import CouriersCreateSerializer, OrdersCreateSerializer
from .services import data_is_valid


@api_view(['POST'])
def couriers_create(request):
    """Принимает POST запрос и валидирует данные"""

    data_list = request.data['data']
    return data_is_valid(data_list, CouriersCreateSerializer, "couriers")


@api_view(['POST'])
def orders_create(request):
    """Принимает POST запрос и валидирует данные"""

    data_list = request.data['data']
    return data_is_valid(data_list, OrdersCreateSerializer, "orders")
