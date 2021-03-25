from datetime import datetime

from rest_framework.response import Response
from rest_framework import status

from .utils import *


def valid_create(ModelSerializer, data_list, model):
    """Возвращает статус валидности запроса (201 или 400)

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


def valid_update(ModelSerializer, courier, fields_dict):
    """Возвращает статус валидности запроса (201 или 400)
    
    ModelSerializer - сериализатор модели для валидации входных данных
    courier - объект курьера, если id имеется в базе, иначе пустой
    fields_dict - список данных для обновления информации

    valid_fields - требуемые поля для заполнения
    taken_fields - поля, переданные в запросе
    
    model_fields - все поля модели
    values_fields - значения всех полей модели
    courier_info - информация о курьере в виде словаря
    """

    if courier:
        if fields_dict:
            serializer = ModelSerializer(
                courier.first(), data=fields_dict, partial=True)

            valid_fields = sorted(serializer.Meta.fields[1:])
            taken_fields = sorted(list(serializer.initial_data.keys()))

            if all(field in valid_fields for field in taken_fields):

                if serializer.is_valid():
                    serializer.save()

                    model_fields = serializer.Meta.fields
                    values_fields = list(courier.values().first().values())

                    courier_info = dict(zip(model_fields, values_fields))

                    return Response(courier_info, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def valid_assign(ModelSerializer, Assign, available_orders, courier, fields_dict):
    """Возвращает статус валидности запроса (201 или 400)

    ModelSerializer - сериализатор модели для валидации входных данных
    Assign - модель, в которой хранятся заказы, выданные курьерам
    
    available_orders - заказы, доступные к выдаче
    courier - объект курьера, если id имеется в базе, иначе пустой
    fields_dict - список полей, переданных в запросе
    
    valid_fields - требуемые поля для заполнения
    taken_fields - поля, переданные в запросе
    
    issues_orders - список выданных заказов
    assign_time - время назначенного заказа
    orders_ids - id's выданных заказов
    """

    if fields_dict:
        serializer = ModelSerializer(data=fields_dict)

        valid_fields = sorted(serializer.Meta.fields)
        taken_fields = sorted(list(serializer.initial_data.keys()))

        if serializer.is_valid() and valid_fields == taken_fields:
            issues_orders = []

            for order in available_orders:
                if order.region in courier.regions:
                    if is_available_order_time(order.delivery_hours, courier.working_hours):
                        max_weight = int(courier.get_courier_type_display())

                        if order.weight + courier.used_weight <= max_weight:
                            issues_orders.append(order)
                            order.is_available = False
                            courier.used_weight += order.weight

                            order.save()
                            courier.save()

            if issues_orders == []:
                return Response({"orders": issues_orders}, status=status.HTTP_201_CREATED)

            assign_time = datetime.utcnow().isoformat()[:-4] + "Z"

            for order in issues_orders:
                Assign.objects.create(courier_id=courier,
                                      order_id=order, assign_time=assign_time)

            orders_ids = [{"id": order.order_id} for order in issues_orders]

            return Response({"orders": orders_ids, "assign_time": assign_time}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)
