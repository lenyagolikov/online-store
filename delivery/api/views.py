from rest_framework.decorators import api_view

from .serializers import CouriersCreateSerializer, CourierUpdateSerializer, OrdersCreateSerializer
from .services import valid_create, valid_update

from ..models import Courier


@api_view(['POST'])
def couriers_create(request):
    """Принимает запрос для создания курьеров"""

    data_list = request.data['data']

    return valid_create(data_list, CouriersCreateSerializer, "couriers")


@api_view(['PATCH'])
def courier_update(request, id):
    """Принимает запрос на изменение полей у курьера с указанным id"""

    courier = Courier.objects.filter(courier_id=id).first()
    fields_list = request.data
    
    return valid_update(fields_list, courier, CourierUpdateSerializer)


@api_view(['POST'])
def orders_create(request):
    """Принимает запрос для создания заказов"""

    data_list = request.data['data']

    return valid_create(data_list, OrdersCreateSerializer, "orders")
