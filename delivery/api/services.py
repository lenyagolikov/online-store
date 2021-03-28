from datetime import datetime

from rest_framework.response import Response
from rest_framework import status

from .utils import *


def valid_create(ModelSerializer, data_list, model):
    """
    Отображает id's, добавленные в базу, при успешной валидации,
    иначе выводит id's, не прошедших валидацию
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
            invalid_ids.append(data[serializer.Meta.fields[0]])

    if invalid_ids == []:

        for data in valid_objects:
            data.save()

        valid_ids_dict = [{"id": data[data.Meta.fields[0]].value}
                          for data in valid_objects]

        return Response({model: valid_ids_dict}, status=status.HTTP_201_CREATED)

    invalid_ids_dict = [{"id": id} for id in invalid_ids]
    return Response({"validation_error": {model: invalid_ids_dict}}, status=status.HTTP_400_BAD_REQUEST)


def valid_update(ModelSerializer, Assign, courier, fields_dict):
    """Возвращает статус валидности запроса на обновление (201 или 400)"""

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
                    if order.region in courier.first().regions:
                        if is_available_order_time(order.delivery_hours, courier.first().working_hours):
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
    """
    Отображает выданные заказы курьеру, которые еще не выполнены
    Если таких заказов нет, выводит пустой список
    """

    serializer = ModelSerializer(data=fields_dict)

    valid_fields = sorted(serializer.Meta.fields)
    taken_fields = sorted(list(serializer.initial_data.keys()))

    if serializer.is_valid() and valid_fields == taken_fields:
        delivery = Assign.objects.filter(
            courier_id=courier.courier_id, completed=False).first()

        if delivery:
            assigned_orders = delivery.orders
            assign_time = delivery.assign_time
        else:
            assigned_orders = []

            for order in available_orders:
                if order.region in courier.regions:
                    if is_available_order_time(order.delivery_hours, courier.working_hours):
                        max_weight = int(courier.get_courier_type_display())
                        current_weight = 0

                        if order.weight + current_weight <= max_weight:
                            assigned_orders.append(order.order_id)
                            order.is_available = False
                            current_weight += order.weight
                            order.save()

            if assigned_orders == []:
                return Response({"orders": assigned_orders}, status=status.HTTP_200_OK)

            assign_time = datetime.utcnow().isoformat()[:-4] + "Z"
            Assign.objects.create(courier_id=courier, courier_type=courier.courier_type,
                                  orders=assigned_orders, assign_time=assign_time)

        orders = [{"id": order_id} for order_id in assigned_orders]

        return Response({"orders": orders, "assign_time": assign_time}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def valid_complete(ModelSerializer, Assign, Order, fields_dict):
    """Отображает заказ, который был помечен, как выполненный"""

    serializer = ModelSerializer(data=fields_dict)

    valid_fields = sorted(serializer.Meta.fields)
    taken_fields = sorted(list(serializer.initial_data.keys()))

    if serializer.is_valid() and valid_fields == taken_fields:
        courier_id = serializer.data['courier_id']
        order_id = serializer.data['order_id']
        complete_time = serializer.data['complete_time']

        delivery = Assign.objects.filter(
            courier_id=courier_id, completed=False).first()

        if delivery and order_id in delivery.orders:
            if complete_time > previous_order_time(Assign, Order, courier_id):
                order = Order.objects.get(order_id=order_id)
                order.complete_time = complete_time
                order.save()

                delivery.orders.remove(order_id)
                delivery.finished_orders.append(order_id)

                if not delivery.orders:
                    delivery.completed = True

                delivery.save()

                return Response({"order_id": order_id}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def courier_info(courier):
    """Возвращает статус валидности запроса на отображение информации о курьере (200 или 400)"""

    if courier:
        fields = list(courier.__dict__.keys())[1:]
        values = list(courier.__dict__.values())[1:]

        courier_info = dict(zip(fields, values))

        return Response(courier_info, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
