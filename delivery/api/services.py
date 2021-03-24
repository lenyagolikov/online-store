from rest_framework.response import Response
from rest_framework import status

from datetime import datetime, time


def valid_create(data_list, ModelSerializer, model):
    """Возвращает статус валидности запроса

    data_list - все json-объекты запроса, хранит поля и их значения
    ModelSerializer - сериализатор модели для валидации
    model - название модели
    valid_objects - список объектов, прошедших валидацию
    invalid_ids - список id's, не прошедших валидацию
    valid_fields - требуемые поля для заполнения
    taken_fields - поля, находящиеся в одном объекте запроса
    valid_ids_dict - представление id, прошедших валидацию, в словаре
    invalid_ids_dict - представление id, не прошедших валидацию, в словаре
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
            invalid_ids.append(serializer[next(iter(serializer.fields))])

    if invalid_ids == []:

        for data in valid_objects:
            data.save()

        valid_ids_dict = [{"id": data[next(iter(data.fields))].value}
                          for data in valid_objects]

        return Response({model: valid_ids_dict}, status=status.HTTP_201_CREATED)

    invalid_ids_dict = [{"id": id.value} for id in invalid_ids]
    return Response({"validation_error": {model: invalid_ids_dict}}, status=status.HTTP_400_BAD_REQUEST)


def valid_update(fields_dict, courier, ModelSerializer):
    """Возвращает статус валидности запроса

    fields_dict - поля и их значения в словаре
    courier - объект курьера, если id имеется в базе, иначе пустой
    ModelSerializer - сериализатор модели для валидации
    valid_fields - требуемые поля для заполнения
    taken_fields - поля, находящиеся в одном объекте запроса
    model_fields - поля модели
    values_fields - значения полей модели
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


def is_right_time(delivery_hours, working_hours):
    """
    Принимает часы доставки заказа и график работы курьера
    Если курьеру удобно принять заказ, то возвращает True, иначе False

    begin_time - начало промежутка
    end_time - конец промежутка
    check_time - проверка, входит ли это время в промежуток
    """

    for delivery_time in delivery_hours:
        check_time = time(int(delivery_time[:2]), int(delivery_time[3:5]))

        for working_time in working_hours:
            begin_time = time(int(working_time[:2]), int(working_time[3:5]))
            end_time = time(int(working_time[6:8]), int(working_time[9:]))

            if begin_time <= check_time <= end_time:
                return True

            begin_time = time(int(delivery_time[:2]), int(delivery_time[3:5]))
            end_time = time(int(delivery_time[6:8]), int(delivery_time[9:]))
            check_time = time(int(working_time[:2]), int(working_time[3:5]))

            if begin_time <= check_time <= end_time:
                return True

    return False


def valid_assign(fields_dict, ModelSerializer, courier, available_orders, Assign):
    """Возвращает статус валидности запроса

    fields_dict - поля и их значения в словаре
    valid_fields - требуемые поля для заполнения
    taken_fields - поля, находящиеся в одном объекте запроса
    courier - объект курьера, найденный по id
    available_orders - заказы, доступные к выдаче
    Assign - таблица, где хранятся курьеры и их заказы
    issues_orders - подходящие заказы
    """

    if fields_dict:
        serializer = ModelSerializer(data=fields_dict)

        valid_fields = sorted(serializer.Meta.fields)
        taken_fields = sorted(list(serializer.initial_data.keys()))

        if serializer.is_valid() and valid_fields == taken_fields:

            issues_orders = []

            for order in available_orders:
                if order.region in courier.regions:
                    if is_right_time(order.delivery_hours, courier.working_hours):
                        max_weight = int(courier.get_courier_type_display())

                        if order.weight + courier.used_weight <= max_weight:
                            issues_orders.append(order.order_id)
                            order.weight = 25
                            order.is_available = False
                            courier.used_weight += order.weight

            if issues_orders == []:
                return Response({"orders": issues_orders}, status=status.HTTP_201_CREATED)

            assign_time = datetime.utcnow().isoformat()[:-4] + "Z"

            Assign.objects.create(
                courier_id=courier, orders_ids=issues_orders, assign_time=assign_time)

            orders_ids = [{"id": order_id} for order_id in issues_orders]

            return Response({"orders": orders_ids, "assign_time": assign_time}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)
