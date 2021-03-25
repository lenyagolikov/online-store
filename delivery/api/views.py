from rest_framework.decorators import api_view

from ..models import *

from .services import valid_create, valid_update, valid_assign
from .serializers import *


@api_view(['POST'])
def couriers_create(request):
    """
    Принимает список с данными о курьерах и загружает их в базу данных
    """

    data_list = request.data.get('data')

    return valid_create(CouriersCreateSerializer, data_list, "couriers")


@api_view(['PATCH'])
def courier_update(request, id):
    """
    Принимает список с данными для изменения информации о курьере
    """

    courier = Courier.objects.filter(courier_id=id)
    fields_dict = request.data

    return valid_update(CourierUpdateSerializer, courier, fields_dict)


@api_view(['POST'])
def orders_create(request):
    """
    Принимает список с данными о заказах и загружает их в базу данных
    """

    data_list = request.data.get('data')

    return valid_create(OrdersCreateSerializer, data_list, "orders")


@api_view(['POST'])
def orders_assign(request):
    """
    Принимает id курьера и назначает максимальное количество заказов,
    подходящих по весу, району и графику работы
    """

    fields_dict = request.data

    courier = Courier.objects.filter(courier_id=fields_dict.get('courier_id')).first()
    available_orders = Order.objects.filter(is_available=True).order_by("weight")

    return valid_assign(OrdersAssignSerializer, Assign, available_orders, courier, fields_dict)
