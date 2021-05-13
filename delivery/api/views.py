from rest_framework.decorators import api_view
from delivery.models import Courier, Order, Assign
from delivery.api import services
from delivery.api import serializers


@api_view(['POST'])
def couriers_create(request):
    """Принимает список с данными о курьерах и загружает их в базу данных"""

    data_list = request.data.get('data')

    return services.valid_create(serializers.CouriersCreateSerializer, data_list, "couriers")


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
        return services.courier_info(Assign, Order, courier)

    if request.method == 'PATCH':
        fields_dict = request.data
        return services.valid_update(serializers.CourierUpdateSerializer, Assign, Order, courier, fields_dict)


@api_view(['POST'])
def orders_create(request):
    """Принимает список с данными о заказах и загружает их в базу данных"""

    data_list = request.data.get('data')

    return services.valid_create(serializers.OrdersCreateSerializer, data_list, "orders")


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

    return services.valid_assign(serializers.OrdersAssignSerializer, Assign, courier, available_orders, fields_dict)


@api_view(['POST'])
def orders_complete(request):
    """
    Принимает id курьера, id заказа и время выполнения заказа
    Отмечает заказ выполненным
    """

    fields_dict = request.data

    return services.valid_complete(serializers.OrdersCompleteSerializer, Assign, Order, fields_dict)
