from rest_framework.decorators import api_view

from ..models import *

from .services import courier_info, valid_complete, valid_create, valid_update, valid_assign
from .serializers import *


@api_view(['POST'])
def couriers_create(request):
    """
    Принимает список с данными о курьерах и загружает их в базу данных
    """

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

    if request.method == 'GET':
        courier = Courier.objects.filter(courier_id=id).first()
        return courier_info(courier)

    if request.method == 'PATCH':
        courier = Courier.objects.filter(courier_id=id)
        fields_dict = request.data
        return valid_update(CourierUpdateSerializer, Assign, courier, fields_dict)


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

    courier - объект курьера, найденный по id
    available_orders - заказы, доступные к выдаче
    """

    fields_dict = request.data

    courier = Courier.objects.filter(
        courier_id=fields_dict.get('courier_id')).first()
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

    return valid_complete(OrdersCompleteSerializer, Assign, Order, Courier, fields_dict)
