from rest_framework.decorators import api_view

from ..models import Courier

from .services import valid_create, valid_update, valid_assign
from .serializers import *


@api_view(['POST'])
def couriers_create(request):
    """
    Принимает список с данными о курьерах
    Возвращает результат функции valid_create
    """

    data_list = request.data['data']

    return valid_create(data_list, CouriersCreateSerializer, "couriers")


@api_view(['PATCH'])
def courier_update(request, id):
    """
    Принимает список полей для изменения информации о курьере, хранит их в словаре
    Возвращает результат функции valid_update
    """

    courier = Courier.objects.filter(courier_id=id)
    fields_dict = request.data

    return valid_update(fields_dict, courier, CourierUpdateSerializer)


@api_view(['POST'])
def orders_create(request):
    """
    Принимает список с данными о заказах
    Возвращает результат функции valid_create
    """

    data_list = request.data['data']

    return valid_create(data_list, OrdersCreateSerializer, "orders")


@api_view(['POST'])
def orders_assign(request):
    """
    Принимает id курьера и назначает максимальное количество заказов,
    подходящих по весу, району и графику работы
    """

    fields_dict = request.data

    return valid_assign(fields_dict, OrderAssignSerializer)
