from rest_framework.response import Response
from rest_framework import fields, status


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

    fields_dict - поля и их значния в словаре
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
