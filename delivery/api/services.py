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


def valid_update(ModelSerializer, Assign, Order, courier, fields_dict):
    """
    Отображает карточку курьера с изменениями
    Если появляются заказы, которые курьер не может развести,
    то такие заказы снимаются и становятся доступными для других курьеров
    """

    if courier:
        if fields_dict:
            serializer = ModelSerializer(
                courier, data=fields_dict, partial=True)

            valid_fields = sorted(serializer.Meta.fields[1:])
            taken_fields = sorted(list(serializer.initial_data.keys()))

            if all(field in valid_fields for field in taken_fields):

                if serializer.is_valid():
                    serializer.save()

                    delivery = Assign.objects.filter(
                        courier_id=courier.courier_id, completed=False).first()

                    if delivery:
                        available_orders = Order.objects.filter(
                            pk__in=delivery.active_orders).order_by('weight')
                        assigned_orders = search_suitable_orders(
                            available_orders, courier)

                        unsuitable_orders = list(
                            set(delivery.active_orders) - set(assigned_orders))

                        for order_id in unsuitable_orders:
                            order = Order.objects.get(order_id=order_id)
                            order.is_available = True
                            order.save()

                            delivery.active_orders.remove(order_id)

                            if not delivery.active_orders:
                                delivery.completed = True

                            delivery.save()

                    model_fields = list(courier.__dict__.keys())[1:5]
                    values_fields = list(courier.__dict__.values())[1:5]

                    courier_info = dict(zip(model_fields, values_fields))

                    return Response(courier_info, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_404_NOT_FOUND)


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
            assigned_orders = delivery.active_orders
            assign_time = delivery.assign_time
        else:
            assigned_orders = search_suitable_orders(available_orders, courier)

            if assigned_orders == []:
                return Response({"orders": assigned_orders}, status=status.HTTP_200_OK)

            assign_time = datetime.utcnow().isoformat()[:-4] + "Z"
            Assign.objects.create(courier_id=courier, courier_type=courier.courier_type,
                                  active_orders=assigned_orders, assign_time=assign_time)

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

        if is_completed_order_found(delivery, order_id, courier_id, complete_time, Assign, Order):
            return Response({"order_id": order_id}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def courier_info(Assign, Order, courier):
    """Отображает информацию о курьере и дополнительную статистику: рейтинг и заработок"""

    if courier:
        calculation_of_earnings(Assign, courier)
        calculation_of_rating(Assign, Order, courier)

        fields = list(courier.__dict__.keys())[1:]
        values = list(courier.__dict__.values())[1:]

        courier_info = dict(zip(fields, values))

        if not courier_info['rating']:
            del courier_info['rating']

        return Response(courier_info, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)
