from rest_framework.response import Response
from rest_framework import status


def valid_create(data_list, ModelSerializer, model):
    """Возвращает статус валидности создания объекта(курьера/заказа)

    data_list - принимаемые данные с запроса
    ModelSerializer - модель класса из БД для сериализации
    model - название модели
    valid_objects - список объектов, прошедших валидацию
    invalid_ids - список id's, не прошедших валидацию
    """

    valid_objects = []
    invalid_ids = []

    for data in data_list:
        serializer = ModelSerializer(data=data)

        if serializer.is_valid():
            valid_objects.append(serializer)
        else:
            invalid_ids.append(serializer[next(iter(serializer.fields))])

    if invalid_ids == []:
        for data in valid_objects:
            data.save()
        return Response({model: [{"id": data[next(iter(data.fields))].value} for data in valid_objects]}, status=status.HTTP_201_CREATED)

    return Response({"validation_error": {model: [{"id": id.value} for id in invalid_ids]}}, status=status.HTTP_400_BAD_REQUEST)


def valid_update(fields_list, courier, ModelSerializer):
    """Возвращает статус валидности изменения информации о курьере"""

    if courier:
        if fields_list:
            serializer = ModelSerializer(
                courier, data=fields_list, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)
