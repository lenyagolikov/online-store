from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Courier, Order
from .serializers import CourierSerializer, OrderSieralizer


@api_view(['POST'])
def couriers_list(request):
    data_list = request.data['data']

    correct_data_list = []
    id_errors_list = []

    for data in data_list:
        serializer = CourierSerializer(data=data)

        if serializer.is_valid():
            correct_data_list.append(serializer)
        else:
            id_errors_list.append(serializer['courier_id'])

    if id_errors_list == []:
        for data in correct_data_list:
            data.save()

        return Response({"couriers": [{"id": data['courier_id'].value} for data in correct_data_list]}, status=status.HTTP_201_CREATED)

    return Response({"validation_error": {"couriers": [{"id": id.value} for id in id_errors_list]}}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def orders_list(request):
    data_list = request.data['data']

    correct_data_list = []
    id_errors_list = []

    for data in data_list:
        serializer = OrderSieralizer(data=data)
        print(data)
        if serializer.is_valid():
            correct_data_list.append(serializer)
        else:
            id_errors_list.append(serializer['order_id'])

    if id_errors_list == []:
        for data in correct_data_list:
            data.save()

            return Response({"orders": [{"id": data['order_id'].value} for data in correct_data_list]}, status=status.HTTP_201_CREATED)

    return Response({"validation_error": {"orders": [{"id": id.value} for id in id_errors_list]}}, status=status.HTTP_400_BAD_REQUEST)
