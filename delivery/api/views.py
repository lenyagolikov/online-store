from rest_framework.decorators import api_view

from ..models import *

from .services import *
from .serializers import *


@api_view(['POST'])
def couriers_create(request):
    """Принимает список с данными о курьерах и загружает их в базу данных"""

    data_list = request.data.get('data')

    return valid_create(CouriersCreateSerializer, data_list, "couriers")


@api_view(['GET', 'PATCH'])
def courier_detail(request, id):
    """
    GET:
    Возвращает информацию о курьере

    PATCH:
    Принимает список с данными для изменения информации о курьере
    """

    courier = Courier.objects.filter(courier_id=id).first()

    if request.method == 'GET':
        return courier_info(Assign, courier)

    if request.method == 'PATCH':
        fields_dict = request.data
        return valid_update(CourierUpdateSerializer, Assign, Order, courier, fields_dict)


@api_view(['POST'])
def orders_create(request):
    """Принимает список с данными о заказах и загружает их в базу данных"""

    data_list = request.data.get('data')

    return valid_create(OrdersCreateSerializer, data_list, "orders")


@api_view(['POST'])
def orders_assign(request):
    """
    Принимает id курьера и назначает максимальное количество заказов,
    подходящих по весу, району и графику работы
    """

    fields_dict = request.data

    courier = Courier.objects.filter(
        courier_id=fields_dict['courier_id']).first()
    available_orders = Order.objects.filter(
        is_available=True).order_by("weight")

    return valid_assign(OrdersAssignSerializer, Assign, courier, available_orders, fields_dict)


@api_view(['POST'])
def orders_complete(request):
    """
    Принимает id курьера, id заказа и время выполнения заказа
    Отмечает заказ выполненным
    """

    fields_dict = request.data

    return valid_complete(OrdersCompleteSerializer, Assign, Order, fields_dict)
