from datetime import datetime

from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status


from .utils import *


def valid_create(ModelSerializer, data_list, model):
    """Возвращает статус валидности запроса на создание (201 или 400)

    ModelSerializer - сериализатор модели для валидации входных данных
    data_list - список с данными о модели
    model - название модели

    valid_objects - список объектов, прошедших валидацию
    invalid_ids - список id's, не прошедших валидацию

    valid_fields - требуемые поля для заполнения
    taken_fields - поля, переданные в запросе

    valid_ids_dict - отображение прошедших валидацию id в словаре
    invalid_ids_dict - отображение не прошедших валидацию id в словаре
    """

    valid_objects = []
    invalid_ids = []

    for data in data_list:
        serializer = ModelSerializer(data=data)

        valid_fields = sorted(serializer.Meta.fields)
        taken_fields = sorted(list(serializer.initial_data.keys()))

        if serializer.is_valid() and valid_fields == taken_fields:
            valid_objects.append(serializer)
        else:
            invalid_ids.append(serializer[next(iter(serializer.data))].value)

    if invalid_ids == []:

        for data in valid_objects:
            data.save()

        valid_ids_dict = [{"id": data[next(iter(data.fields))].value}
                          for data in valid_objects]

        return Response({model: valid_ids_dict}, status=status.HTTP_201_CREATED)

    invalid_ids_dict = [{"id": id} for id in invalid_ids]
    return Response({"validation_error": {model: invalid_ids_dict}}, status=status.HTTP_400_BAD_REQUEST)


def valid_update(ModelSerializer, Assign, courier, fields_dict):
    """Возвращает статус валидности запроса на обновление (201 или 400)

    ModelSerializer - сериализатор модели для валидации входных данных
    courier - объект курьера в queryset, если id имеется в базе, иначе пустой
    fields_dict - список данных для обновления информации
    Assign - модель, в которой хранятся заказы, выданные курьерам

    valid_fields - требуемые поля для заполнения
    taken_fields - поля, переданные в запросе

    outstanding_orders - невыполненные заказы курьера
    issues_orders - подходящие заказы
    unsuitable_orders - неподходящие заказы после изменения информации о курьере

    model_fields - все поля модели
    values_fields - значения всех полей модели
    courier_info - информация о курьере в виде словаря
    """

    if courier and fields_dict:
        serializer = ModelSerializer(
            courier.first(), data=fields_dict, partial=True)

        valid_fields = sorted(serializer.Meta.fields[1:])
        taken_fields = sorted(list(serializer.initial_data.keys()))

        if all(field in valid_fields for field in taken_fields):

            if serializer.is_valid():
                serializer.save()

                assigns = Assign.objects.filter(
                    courier_id=courier.first().courier_id, complete_time=None).order_by('order_id__weight')

                outstanding_orders = [assign.order_id for assign in assigns]
                issues_orders = []

                for order in outstanding_orders:
                    if order.region in courier.first().regions and is_available_order_time(order.delivery_hours, courier.first().working_hours):
                        max_weight = int(
                            courier.first().get_courier_type_display())
                        current_weight = 0

                        if order.weight + current_weight <= max_weight:
                            issues_orders.append(order)
                            current_weight += order.weight

                unsuitable_orders = list(
                    set(outstanding_orders) - set(issues_orders))

                for order in unsuitable_orders:
                    Assign.objects.filter(
                        courier_id=courier.first().courier_id, order_id=order.order_id).delete()
                    order.is_available = True
                    order.save()

                model_fields = serializer.Meta.fields
                values_fields = list(courier.values().first().values())

                courier_info = dict(zip(model_fields, values_fields))

                return Response(courier_info, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def valid_assign(ModelSerializer, Assign, courier, available_orders, fields_dict):
    """Возвращает статус валидности запроса на связывание заказа с курьером (201 или 400)"""

    serializer = ModelSerializer(data=fields_dict)

    valid_fields = sorted(serializer.Meta.fields)
    taken_fields = sorted(list(serializer.initial_data.keys()))

    if serializer.is_valid() and valid_fields == taken_fields:
        current_courier = Assign.objects.filter(courier_id=courier.courier_id, completed=False)

        if current_courier:
            current_orders = current_courier.first().orders_ids
        else:
            current_orders = []

        if courier.is_available:
            for order in available_orders:
                if order.region in courier.regions and is_available_order_time(order.delivery_hours, courier.working_hours):
                    max_weight = int(courier.get_courier_type_display())
                    current_weight = 0

                    if order.weight + current_weight <= max_weight:
                        current_orders.append(order.order_id)
                        order.is_available = False
                        courier.is_available = False
                        current_weight += order.weight
                        order.save()
                        courier.save()

        if current_orders == []:
            return Response({"orders": current_orders}, status=status.HTTP_201_CREATED)

        if current_courier:
            assign_time = current_courier.first().assign_time
        else:
            assign_time = datetime.utcnow().isoformat()[:-4] + "Z"

            Assign.objects.create(courier_id=courier, courier_type=courier.courier_type,
                                  orders_ids=current_orders, assign_time=assign_time)

        orders_ids_dict = [{"id": order_id}
                           for order_id in current_orders]

        return Response({"orders": orders_ids_dict, "assign_time": assign_time}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def valid_complete(ModelSerializer, Assign, Order, Courier, fields_dict):
    """Возвращает статус валидности запроса на отметку заказа выполненым (201 или 400)"""

    serializer = ModelSerializer(data=fields_dict)

    valid_fields = sorted(serializer.Meta.fields)
    taken_fields = sorted(list(serializer.initial_data.keys()))

    if serializer.is_valid() and valid_fields == taken_fields:
        courier_id = serializer.data['courier_id']
        order_id = serializer.data['order_id']
        complete_time = serializer.data['complete_time']

        current_courier = Assign.objects.filter(
            courier_id=courier_id, completed=False).first()

        if current_courier:
            courier_orders = current_courier.orders_ids

            if order_id in courier_orders:
                order = Order.objects.get(order_id=order_id)
                order.complete_time = complete_time
                order.save()

                current_courier.orders_ids.remove(order_id)
                current_courier.completed_orders_ids.append(order_id)

                if not current_courier.orders_ids:
                    current_courier.completed = True
                    courier = Courier.objects.get(courier_id=courier_id)
                    courier.is_available = True
                    courier.save()

                current_courier.save()

                return Response({"order_id": order_id}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def courier_info(courier):
    """Возвращает статус валидности запроса на отображение информации о курьере (200 или 400)

    courier - объект курьера

    fields - поля курьера в модели
    values - значения курьера в модели
    courier_info - отображение информации в словаре
    """

    if courier:
        fields = list(courier.__dict__.keys())[1:]
        values = list(courier.__dict__.values())[1:]

        courier_info = dict(zip(fields, values))

        return Response(courier_info, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
